---
name: gh-pages-landing
description: Research, shape, design, build, and validate a project-specific landing page from repository evidence and audience needs, then hand prepared static output to github-pages-legacy-deploy when publication is requested. Use for repository homepages, product landing pages, GitHub Pages redesigns, and substantial landing-page iterations that must remain truthful, responsive, interactive, and distinctive.
---

# Project-Driven Landing Pages

## Role and boundary

Create a truthful product argument, not a themed README or generic section template. This skill owns discovery, copy architecture, module selection, visual design, interaction and motion, implementation, and browser validation. It does **not** configure or publish GitHub Pages; when publication is authorized, hand prepared output to `github-pages-legacy-deploy`.

Assume the model can design. Preserve room for judgment and invention; prescribe methods only where failure would break truth, safety, usability, authorization, or observable quality.

## Constraint model

Read `references/workflow-and-freedom.md` for substantial new pages or redesigns.

These invariants always apply:

- Claims, numbers, commands, interfaces, and product states must be traceable to repository or runtime evidence. Label synthetic data and simulated behavior.
- Do not expose secrets or private data, and do not infer permission to deploy, commit, push, or overwrite.
- Core content remains readable without JavaScript. Keyboard access, visible focus, usable contrast, and touch targets are required.
- Design desktop, intermediate, and narrow-mobile compositions deliberately. A compressed desktop layout is not mobile design.
- Respect `prefers-reduced-motion`; motion must not block reading or operation.
- Validate the rendered page and real interactions before claiming completion.

Everything else is a design decision, not a universal law. Section count, layout family, card use, technology, motion count, visual style, and number of proposals should follow the project and selected freedom mode.

## Choose the working mode

For a new page or substantial redesign, ask once which creative-freedom mode the user wants. Recommend **guided** unless context clearly supports another choice. Do not re-ask for local fixes or when a mode is already established.

- **Autonomous:** inspect first, present a compact brief, then make design and motion decisions independently. Ask only about material product ambiguity.
- **Guided (default):** confirm (1) copy/narrative and (2) module, state, interaction, and mobile-equivalence plan. The model owns detailed visual and motion decisions.
- **Strict:** pause at additional visual, responsive, and motion gates when brand risk or an explicit user request warrants it.

Use a light version of `grill-me`: investigate before asking; ask one decision-changing question at a time; include a recommended answer and tradeoff; probe contradictions; stop once the decisions required by the selected mode are resolved. Never ask for facts the repository can prove.

## Outcome-driven pipeline

The order matters, but depth and approval count adapt to task size and freedom mode.

### 1. Evidence and product intent

Read `README.md`, manifests, site entry points, the smallest source subset that proves workflows and limits, and real assets. Translate feature → user outcome, verify claims, and record tone signals. Read `references/discovery-and-brief.md`.

Produce a compact evidence dossier and resolve: primary audience, single primary action, core promise, principal trust barrier, voice, and mobile priority.

### 2. Copy and narrative

Write the actual headline, lead, key claims, evidence, and narrative sequence before choosing page furniture. Every section must advance the visitor from arrival to understanding, trust, or action.

In guided mode, this is approval gate one. In autonomous mode, show it as part of the brief without forcing a pause unless it exposes material ambiguity.

### 3. Content-to-module architecture

Read `references/content-to-modules.md`. Map each necessary claim to the smallest useful module or proof surface. Define its narrative job, visible content, evidence, states, interaction, desktop role, narrow-mobile equivalent, motion behavior, and fallback.

Remove modules with no narrative job. Do not default to hero + three cards + bento + FAQ, and do not design a mock merely to fill space.

In guided mode, this is approval gate two. Approve the module inventory and state model before detailed layout or production implementation.

### 4. Visual and responsive composition

Read `references/design-directions.md` and `references/responsive-choreography.md`. Derive a visual system from project tone and approved modules. Define type, color, geometry, density, rhythm, CTA morphology, and compositions for desktop, intermediate, and narrow mobile.

Offer multiple creative directions only when there is a meaningful unresolved branch. If the project already has a clear language, propose one evidence-backed recommendation instead of manufacturing alternatives.

Use installed `design-taste-frontend` as a judgment reference when helpful. Reinterpret reference principles; do not copy protected assets, text, logos, or layouts.

### 5. Interaction and motion contract

Read `references/motion-choreography.md`. Motion must communicate hierarchy, causality, state, or feedback. For each dynamic module define entry, exit/re-entry, user trigger, end state, replay/loop policy, offscreen behavior, mobile behavior, and reduced-motion behavior.

Establish a clear motion hierarchy. Usually one scene carries the strongest narrative emphasis while supporting motion stays quieter; use more than one strong scene only when distinct product mechanisms genuinely require it.

### 6. Build in vertical slices

Read `references/mock-craft.md` when the page includes product surfaces. Implement one representative module end-to-end first: copy, desktop, mobile, interaction, motion, reduced motion, and browser proof. Once the system works, extend it to the remaining page. Preserve the repository's existing stack unless a dependency earns its cost.

## Runtime acceptance

Static checks prove only that code exists. Also verify observable behavior:

- Render at representative desktop, 768px, and 390px widths; test both themes when supported.
- Check headline wrapping, first-screen hierarchy, CTA visibility, horizontal overflow, clipping, and touch ergonomics.
- Scroll into, out of, and back into animated modules. Confirm entry/re-entry behavior and that intended loops continue over time and pause offscreen when appropriate.
- Exercise clicks, keyboard operation, theme/language controls, dynamic panels, and failure/fallback states.
- Test `prefers-reduced-motion` and no-JavaScript readability.
- Inspect the console and failed network requests.
- Verify computed or DOM state changes; keyframes, observers, or class names alone are not proof that motion was visible.

Use `scripts/validate_page.py` for static validation, then perform browser acceptance:

```bash
python3 scripts/validate_page.py <path-to-html>
```

## Publication

Publication requires explicit authorization. For GitHub Pages, hand off to `github-pages-legacy-deploy` and preserve its deployment boundaries. Prepared output may also target another static host, but validate base paths, routing, canonical URLs, and platform-specific redirects separately.

## Desktop product landings (iSparta-style)

When the page promotes an **existing desktop/Electron app**, add these decisions after the generic pipeline:

- **Tokens first.** Read the app's `tokens.css` / theme variables / screenshots. The landing should look like the product on a good day, not a second brand.
- **Product mock, not tutorial chrome.** Task cards, size gates, path/name pickers should mirror real component structure and field names. Copy states **what the feature does**; interaction lives in the control. Do not write "click chips to…" section copy.
- **i18n + theme parity.** If the app has `uiTheme` / locales, ship landing toggles (light/dark/system, zh/en) with a pre-paint theme script to avoid flash. Persist under the same storage keys when it helps continuity.
- **Never leak private sample data.** Paths, folder names, and token demos must be generic (or scrubbed). Ask if unsure.
- **Lineage & credits.** Forked OSS products need a short lineage strip (original → forks → this repo) and an author wall with links.
- **Download links must track latest.** Prefer `releases/latest/download/<stable-name>` and/or resolve the GitHub Releases API at runtime to set `href`s. Avoid hardcoding `vX.Y.Z` in landing CTAs.
- **SEO minimum.** Title/description with product keywords, canonical, Open Graph/Twitter, `SoftwareApplication` JSON-LD, `robots.txt`, `sitemap.xml`, and a README link to the landing. Mention repo Topics/homepage for search discovery.

Hand off publication to `github-pages-legacy-deploy` (legacy docs/branch) **or** an Actions `deploy-pages` workflow when the repo already uses workflow Pages.

## References

- `references/workflow-and-freedom.md` — freedom modes, questioning rules, gates, and invariant priority.
- `references/discovery-and-brief.md` — evidence dossier, copy translation, narrative, and voice.
- `references/content-to-modules.md` — claim-to-module map and module contract.
- `references/design-directions.md` — visual direction and design-system judgment.
- `references/responsive-choreography.md` — desktop/mobile equivalence and responsive state design.
- `references/motion-choreography.md` — motion contracts, replay/loop behavior, and runtime proof.
- `references/mock-craft.md` — truthful dynamic mocks and proof surfaces.
- `references/frontend-design.md` — implementation and accessibility fundamentals.
- `references/github-pages-deploy.md` — handoff to deploy skill (legacy or Actions).
- `scripts/validate_page.py` — static HTML and external-resource checks.
