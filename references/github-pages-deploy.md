# GitHub Pages 发布交接

`gh-pages-landing` 只负责设计、构建和页面验收。它不维护第二套 GitHub Pages API 命令或发布脚本。

## 选哪条发布路径

先看仓库 **已有** 的 Pages 配置（`gh api repos/OWNER/REPO/pages`），再选一条，不要擅自切换 source：

| 路径 | 适用 | 交给谁 |
| --- | --- | --- |
| **Legacy `docs` / `gh-pages`** | 仓库还在用分支源 | `github-pages-legacy-deploy` |
| **Actions `workflow` Pages** | 已是或愿意改成 `build_type: workflow` | 本仓库维护的 `pages.yml`（`actions/deploy-pages`） |

`build_type: workflow` 时用：

```yaml
# .github/workflows/pages.yml
on:
  push:
    branches: [master]
    paths: ['landing/**', '.github/workflows/pages.yml']
  workflow_dispatch:
permissions:
  contents: read
  pages: write
  id-token: write
jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with:
          path: landing   # 或 docs / dist
      - id: deployment
        uses: actions/deploy-pages@v4
```

首次启用（Pages 尚未存在时）：

```bash
gh api -X POST repos/OWNER/REPO/pages -F build_type=workflow
# 已存在则确认： gh api repos/OWNER/REPO/pages --jq '.build_type,.html_url'
```

推送后 `gh workflow run pages.yml` 或依赖 push 触发；用 `html_url` 做 HTTP 200 与关键文案校验。

## Legacy 交接契约

页面完成并经用户授权提交/推送后，调用 `github-pages-legacy-deploy`：

- 用 `docs` 模式发布已推送的 `main:/docs`（仓库站点的默认选择）。
- 只有在产物必须与源码隔离时才用 `branch` 模式；替换已有 `gh-pages` 需要用户明确授权 `--force`。

交接信息必须包含 owner/repo、选定的 mode、branch/path、已推送的页面文件或 include 列表，以及一段页面中可见的 `--expect` 文字。部署 skill 负责创建/更新 legacy Pages 配置、读取真实 `html_url`、轮询并验证内容。

不要依据 GitHub Pages API 默认值推断 build type、source path 或公开 URL。不要在未经确认的情况下切换已有 Pages source。

## 落地页侧额外校验（两条路径共用）

- `index.html` 内相对资源（css/js/图）在 `html_url` 基路径下可 200（项目页前缀如 `/repo-name/`）。
- `robots.txt`、`sitemap.xml` 使用绝对 URL，且与 canonical / `og:url` 一致。
- 下载 CTA 若指向 `releases/latest/download/...`，确认该 Release 上确有同名资产，或页面有 API 回退。
