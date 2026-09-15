#!/usr/bin/env python3
"""Validate a self-contained GitHub Pages landing page.

Usage:
  python3 validate_page.py /path/to/index.html

Checks:
  - parses as HTML and has required document elements
  - rejects external runtime resources by default; --allow-cdn permits reviewed script CDNs only
  - requires viewport, title, h1, main, reduced-motion CSS, focus-visible CSS
  - requires aria labels on icon/copy buttons
  - optionally runs `node --check` on inline JavaScript when Node is available

For runtime interaction verification, use jsdom from a managed Node workspace:
  const {JSDOM}=require('jsdom');
  new JSDOM(fs.readFileSync(page,'utf8'), {runScripts:'dangerously', pretendToBeVisual:true});
Then inspect key DOM counts and dispatch click events on copy buttons.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import urlparse
from html.parser import HTMLParser
from pathlib import Path

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
APPROVED_CDN_HOSTS = {"cdn.jsdelivr.net", "unpkg.com", "cdnjs.cloudflare.com"}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, int]] = []
        self.errors: list[str] = []
        self.tags: set[str] = set()
        self.attrs: list[tuple[str, dict[str, str | None]]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.add(tag)
        attr_map = dict(attrs)
        self.attrs.append((tag, attr_map))
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.add(tag)
        self.attrs.append((tag, dict(attrs)))

    def handle_endtag(self, tag: str) -> None:
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f"unexpected closing </{tag}> at line {self.getpos()[0]}")
            return
        # SVG children are valid HTML but HTMLParser can report them loosely.
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                return
        self.errors.append(f"closing </{tag}> without opener at line {self.getpos()[0]}")


def fail(msg: str, errors: list[str]) -> None:
    errors.append(msg)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("html", type=Path)
    ap.add_argument("--allow-cdn", action="store_true", help="allow version-pinned HTTPS scripts from approved CDNs")
    args = ap.parse_args()
    page = args.html.expanduser().resolve()
    if not page.is_file():
        print(f"ERROR: file not found: {page}", file=sys.stderr)
        return 2

    text = page.read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(text)
    errors = list(parser.errors)
    if parser.stack:
        errors.extend(f"unclosed <{tag}> opened near line {line}" for tag, line in parser.stack[-10:])

    for tag in ("html", "head", "body", "title", "main", "h1"):
        if tag not in parser.tags:
            fail(f"missing required <{tag}> element", errors)

    if not any(tag == "meta" and attrs.get("name") == "viewport" for tag, attrs in parser.attrs):
        fail("missing viewport meta", errors)

    for tag, attrs in parser.attrs:
        if tag in ("script", "img", "iframe", "video", "audio", "source") and attrs.get("src"):
            src = attrs["src"] or ""
            parsed = urlparse(src)
            allowed_cdn = (
                args.allow_cdn
                and tag == "script"
                and parsed.scheme == "https"
                and parsed.hostname in APPROVED_CDN_HOSTS
                and (
                    "@" in parsed.path  # jsDelivr/unpkg package@version form
                    or bool(re.search(r"/ajax/libs/[^/]+/\d+\.\d+", parsed.path))  # cdnjs library/version form
                )
            )
            is_remote = bool(parsed.scheme) or src.startswith("//")
            if is_remote and not allowed_cdn:
                fail(f"external resource forbidden: <{tag} src={src!r}>", errors)
        if tag == "link" and attrs.get("rel") in ("stylesheet", "preload", "modulepreload") and attrs.get("href"):
            fail(f"external stylesheet/preload forbidden: {attrs['href']}", errors)
        if tag == "button" and (attrs.get("class") or "").find("copy") >= 0 and not attrs.get("aria-label"):
            fail("copy button missing aria-label", errors)

    has_copy_button = any(tag == "button" and "copy" in (attrs.get("class") or "") for tag, attrs in parser.attrs)
    required_snippets = {
        "prefers-reduced-motion": "missing reduced-motion fallback",
        ":focus-visible": "missing keyboard focus-visible style",
    }
    if has_copy_button:
        required_snippets["navigator.clipboard"] = "missing clipboard implementation"
    for snippet, message in required_snippets.items():
        if snippet not in text:
            fail(message, errors)

    scripts = re.findall(r"<script(?:\s[^>]*)?>(.*?)</script>", text, re.S | re.I)
    node = shutil.which("node")
    if scripts and node:
        with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8", delete=False) as fh:
            fh.write("\n;\n".join(scripts))
            js_path = Path(fh.name)
        try:
            result = subprocess.run([node, "--check", str(js_path)], capture_output=True, text=True)
            if result.returncode:
                fail("inline JavaScript syntax error:\n" + result.stderr.strip(), errors)
        finally:
            js_path.unlink(missing_ok=True)

    if errors:
        print(f"FAIL {page}")
        for item in errors:
            print(f"  - {item}")
        return 1

    print(f"PASS {page}")
    print(f"  size: {page.stat().st_size} bytes")
    print(f"  inline scripts: {len(scripts)}")
    print(f"  external runtime resources: {'approved CDN scripts allowed' if args.allow_cdn else '0'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
