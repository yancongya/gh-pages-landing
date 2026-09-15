# 实现基础：排版、色彩与可访问性

本参考覆盖写码阶段的基础工程约定（token、字体、可访问性、复制按钮、CSS 级反模式）。**设计方向与结构推导在动手前完成**——见 `design-directions.md`（Stage C）；这里的布局示例仅是"终端美学"方向的一种可能结构，不是默认模板。

## 1. 先定设计方向（design direction）

不要上来就写居中 hero + 紫色渐变 + 三列卡片——那是"AI 味"模板。方向由创意简报与 Design Read 决定（流程见 `discovery-and-brief.md` 与 `design-directions.md`），本文件不负责选方向，只负责把选定方向实现好。三个自检问题：

1. **产品是什么气质？** CLI/agent 工具 → dev-tool 终端美学；消费产品 → 柔和、大图；B 端 SaaS → 克制、表格化。
2. **用户第一眼要相信什么？** 对工具类：相信"它真的能用"→ 放真实终端输出/真实数据，而不是空洞 slogan。
3. **一句话价值主张是什么？** 把它做成 h1，产品名反而降级为 eyebrow/品牌位。例："对 AI 说一句话，清出 Mac 里沉睡的空间。"

常见可复用方向：
- **终端美学**（本模板默认）：深色优先、等宽字体标签、终端 mockup、真实命令输出。适合一切开发者工具。
- **编辑排版风**：大字号衬线标题 + 大量留白。适合内容/文档产品。
- **Bento 网格**：非对称卡片拼版展示特性，现代且信息密度高。

## 2. 排版与色彩系统

- CSS 变量语义化命名：`--bg / --panel / --ink / --muted / --subtle / --border / --accent`，组件里禁止散落裸 hex。
- 浅/深色两套 `@media (prefers-color-scheme: dark)`，逐变量对照检查对比度（正文 ≥4.5:1）。
- 字体：系统栈正文 + `ui-monospace` 等宽做标签/命令/数字；mono 小标签（大写、letter-spacing .1em+）是 dev-tool 感的核心。
- 基础字号 15–16px，行高 1.5–1.65；标题用 `clamp()` 流式缩放。

## 3. 布局结构（终端美学方向的一种示例架构）

> ⚠️ 这是一套**示例**，仅当 Design Read 判定为终端美学且叙事弧匹配时才可采用。结构必须按 `design-directions.md` C3 的推导流程为每个项目重新推导，禁止无审查地整体照抄。

1. **Hero 左右分栏**：左侧 eyebrow 徽章 → h1（利益点）→ lead（说清这是什么）→ 主 CTA（复制型按钮）+ 次 CTA → 真实数据条；右侧**终端 mockup**（见动画 1）。
2. **类别 marquee**：一行技术关键词无缝滚动，传递"覆盖面"。
3. **编号分区**：`// 01 — 工作方式` 这类 mono 标签 + h2 + sub，节奏感强。
4. **Bento 特性网格**：`grid-template-columns: repeat(3,1fr)`，重点卡 `span 2`；≤960px 改 2 列，≤640px 改 1 列且 span 取消。
5. **表格区**：信息密度高的对比内容（风险级别）用表格而非卡片。
6. **快速开始**：可复制的 prompt/命令块，step 0 用强调边框（`box-shadow: 0 0 0 3px var(--accent-soft)`）。

## 4. 动画模式（纯 CSS 实现级）

> 编舞决策（意图分类、分幕脚本、signature moment）在 `motion-choreography.md`；本节只是可复制的 CSS 实现片段。

### 终端逐行 reveal

```css
.tl{opacity:0; animation:tlin .45s ease forwards; animation-delay:var(--d,0s)}
@keyframes tlin{from{opacity:0; transform:translateY(5px)} to{opacity:1; transform:none}}
```

每行 `<div class="tl" style="--d:.4s">` 递增延迟。光标：`.cursor{animation:blink 1.05s steps(1) infinite}` + `@keyframes blink{50%{opacity:0}}`。

### 无缝 marquee

内容**完整复制两份**（第二份 `aria-hidden="true"`），轨道 `width:max-content`，`animation:mscroll 34s linear infinite` + `@keyframes mscroll{to{transform:translateX(-50%)}}`；`hover` 时 `animation-play-state:paused`。

### 降级（必须）

```css
@media (prefers-reduced-motion: reduce){
  html{scroll-behavior:auto}
  .m-track{animation:none} .marquee{overflow-x:auto}
  .tl{opacity:1; animation:none} .cursor{animation:none}
}
```

## 5. 复制按钮模式（可靠版）

- 精确文本放按钮的 `data-text` 属性；没有时才退化到 `parentElement.innerText.replace(/^复制\s*/,'')`。
- `navigator.clipboard.writeText` 失败时（`file://`、无权限）用隐藏 textarea + `execCommand('copy')` 兜底。
- 反馈：临时改文案"已复制"并加 `.done` 类（变色），1.4s 还原。

### CTA 实现检查

- 在同一张长截图里同时查看页头、Hero 和终章 CTA，不要只审一个组件。
- 如果三处都是“实心 accent 色 + 白色粗体 + 圆角 + hover 阴影”，先停止编码，回到 Design Read 重新分配形态。
- 文字链接也要保持 ≥44px 可点击高度和明确的 `:focus-visible`；“不像按钮”不能牺牲可访问性。

## 6. 可访问性清单（上线前逐项过）

- [ ] skip link（`position:absolute; left:-9999px`，`:focus` 时可见）
- [ ] 标题层级 h1→h2→h3 不跳级
- [ ] 图标按钮必有 `aria-label`；装饰性元素 `aria-hidden="true"`
- [ ] 信息不只靠颜色传达（风险标签 = 色点 + 文字）
- [ ] 触控目标 ≥44px；`:focus-visible` 有 2px 描边
- [ ] `prefers-reduced-motion` 全动画降级
- [ ] 装饰性终端/图示用 `role="img"` + 描述性 `aria-label`

## 7. 反模式（踩过的坑）

- 外链 CDN 框架（Tailwind/Alpine）→ 沙箱预览白屏；`file://` 下兄弟 `<script src>` 时序不可靠 → **一切内联**。
- 用 innerText 当复制内容 → 混入注释和按钮文案 → 用 `data-text`。
- 表格 `min-width` 无条件生效 → 小屏横向滚动 → `min-width` 只在大屏媒体查询里生效，小屏切卡片视图。
- 用 emoji 当图标 → 用内联 SVG（Lucide 风格 stroke 图标）。
- 页头、Hero、终章全部复制高饱和实心圆角 CTA → 按语境分化为导航出口、主操作和叙事收束链接。
