# GitHub Pages 发布交接

`gh-pages-landing` 只负责设计、构建和页面验收。它不维护第二套 GitHub Pages API 命令或发布脚本。

页面完成并经用户授权提交/推送后，调用 `github-pages-legacy-deploy`：

- 用 `docs` 模式发布已推送的 `main:/docs`（仓库站点的默认选择）。
- 只有在产物必须与源码隔离时才用 `branch` 模式；替换已有 `gh-pages` 需要用户明确授权 `--force`。

交接信息必须包含 owner/repo、选定的 mode、branch/path、已推送的页面文件或 include 列表，以及一段页面中可见的 `--expect` 文字。部署 skill 负责创建/更新 legacy Pages 配置、读取真实 `html_url`、轮询并验证内容。

不要依据 GitHub Pages API 默认值推断 build type、source path 或公开 URL。不要在未经确认的情况下切换已有 Pages source。
