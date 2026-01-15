# WeChat Article Publisher Skill

<p align="center">
  <strong>English</strong> | <a href="#中文文档">中文</a>
</p>

> Publish Markdown or HTML articles to WeChat Official Account drafts with one command. Say goodbye to tedious copy-paste-format workflows.

**v1.1.0** — API-based publishing for reliability and speed

---

## The Problem

If you write in Markdown, publishing to WeChat Official Account (公众号) is a **painful process**:

| Pain Point | Description |
|------------|-------------|
| **Format Loss** | Copy from Markdown editor -> Paste to WeChat -> All formatting gone |
| **Manual Formatting** | Re-apply each H2, bold, link manually — 15-20 min per article |
| **Image Upload Hassle** | Upload images one by one through WeChat's media library |
| **Multiple Steps** | Switch between markdown editor, image uploads, and WeChat admin panel |

### Time Comparison

| Task | Manual | With This Skill |
|------|--------|-----------------|
| Format conversion | 15-20 min | 0 (automatic) |
| Image upload | 5-10 min | 0 (automatic) |
| Copy & paste content | 2-3 min | 0 (automatic) |
| **Total** | **20-30 min** | **< 1 min** |

**30x efficiency improvement**

---

## The Solution

This skill uses WeChat's API for direct, reliable publishing:

```
Markdown/HTML File
     | Python parsing
     v
Structured Data (title, content, images)
     | WeChat API
     v
Draft in WeChat Official Account (never auto-publishes)
```

### Key Features

- **API-Based**: Direct API calls, no browser automation needed
- **Cross-Platform**: Works on macOS, Linux, and Windows
- **Dual Format**: Supports both Markdown (.md) and HTML (.html) files
- **Format Preserved**: HTML formatting preserved, Markdown auto-converted
- **Image Auto-Upload**: Images in your content are automatically uploaded
- **Safe by Design**: Only saves as draft, never publishes automatically
- **小绿书 Support**: Publish as image-text format (newspic) for visual content

---

## Requirements

| Requirement | Details |
|-------------|---------|
| Claude Code | [claude.ai/code](https://claude.ai/code) |
| Python 3.9+ | Standard library only (no extra dependencies) |
| WECHAT_API_KEY | Get from [wx.limyai.com](https://wx.limyai.com) |
| WeChat Account | Authorized on wx.limyai.com |

---

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/iamzifei/wechat-article-publisher-skill.git
```

### Step 2: Copy Skill to Claude

```bash
cp -r wechat-article-publisher-skill/skills/wechat-article-publisher ~/.claude/skills/
```

### Step 3: Configure API Key

```bash
cd wechat-article-publisher-skill
cp .env.example .env
# Edit .env and set your WECHAT_API_KEY
```

---

## Usage

### Natural Language

```
把 /path/to/article.md 发布到微信公众号
```

```
Publish ~/Documents/my-post.md to WeChat
```

```
帮我把这篇文章发到公众号：~/articles/ai-tools.md
```

```
把这个HTML文章发布到公众号：~/newsletter/issue-01.html
```

```
Publish the HTML article ~/export/formatted-post.html to WeChat
```

### Skill Command

```
/wechat-article-publisher /path/to/article.md
```

```
/wechat-article-publisher /path/to/article.html
```

### With Options

```
# Publish as 小绿书 (image-text mode)
/wechat-article-publisher /path/to/article.md --type newspic
```

---

## Workflow Steps

```
[1/4] Check API Key...
      -> Load WECHAT_API_KEY from .env

[2/4] List WeChat Accounts...
      -> Find authorized accounts
      -> Auto-select if only one, ask if multiple

[3/4] Publish Article...
      -> Detect file format (Markdown or HTML)
      -> Parse content (title, body, images)
      -> Call WeChat API
      -> Upload images automatically

[4/4] Report Result...
      -> Show success message
      -> Remind to review and publish manually
```

---

## Supported Formats

### Markdown (.md)

| Syntax | Result |
|--------|--------|
| `# H1` | Article title (extracted, not in body) |
| `## H2` | Section headers |
| `### H3` | Sub-section headers |
| `**bold**` | **Bold text** |
| `*italic*` | *Italic text* |
| `[text](url)` | Hyperlinks |
| `> quote` | Blockquotes |
| `- item` | Unordered lists |
| `1. item` | Ordered lists |
| ``` code ``` | Code blocks |
| `![](img.jpg)` | Images (auto-uploaded) |

### HTML (.html)

| Element | Result |
|---------|--------|
| `<title>` or `<h1>` | Article title |
| `<h2>`, `<h3>` | Section headers |
| `<strong>`, `<b>` | **Bold text** |
| `<em>`, `<i>` | *Italic text* |
| `<a href="">` | Hyperlinks |
| `<blockquote>` | Blockquotes |
| `<ul>`, `<ol>` | Lists |
| `<table>` | Tables (preserved) |
| `<img src="">` | Images (auto-uploaded) |
| Inline styles | Preserved |

---

## Article Types

### news (Default)
Standard WeChat article format with full rich text support.

### newspic (小绿书)
Image-focused format for visual content:
- Up to 20 images extracted from content
- Text limited to 1000 characters
- Perfect for photo-heavy posts

---

## Example

### Input: `article.md`

```markdown
# 5 AI Tools Worth Watching in 2024

![cover](./images/cover.jpg)

AI tools exploded in 2024. Here are 5 worth your attention.

## 1. Claude: Best Conversational AI

**Claude** by Anthropic excels at long-context understanding.

> Claude's context window reaches 200K tokens.

![claude-demo](./images/claude-demo.png)
```

### Command

```
把 ~/Documents/article.md 发布到微信公众号
```

### Result

```
✓ 文章已成功发布到公众号草稿箱！

标题: 5 AI Tools Worth Watching in 2024
状态: 已保存到草稿箱

请登录微信公众平台预览并发布。
```

---

## Project Structure

```
wechat-article-publisher-skill/
├── .claude-plugin/
│   └── plugin.json              # Plugin config
├── skills/
│   └── wechat-article-publisher/
│       ├── SKILL.md             # Skill instructions
│       └── scripts/
│           ├── wechat_api.py    # WeChat API client
│           └── parse_markdown.py # Markdown parser
├── docs/
│   └── GUIDE.md                 # Detailed guide
├── .env.example                 # Environment template
├── README.md                    # This file (bilingual)
└── LICENSE
```

---

## FAQ

**Q: How do I get a WECHAT_API_KEY?**
A: Register at [wx.limyai.com](https://wx.limyai.com), authorize your WeChat Official Account, and get your API key from the dashboard.

**Q: Can I publish to multiple accounts?**
A: Yes! If you have multiple authorized accounts, the skill will ask you to choose which one to publish to.

**Q: What happens to my images?**
A: Images are automatically uploaded to WeChat's servers. Both local paths and URLs are supported.

**Q: Will this auto-publish my article?**
A: No, never. Articles are always saved as drafts. You must manually publish from the WeChat admin panel.

**Q: What's the difference between news and newspic?**
A: `news` is standard article format; `newspic` (小绿书) is image-focused with limited text, similar to Instagram posts.

**Q: Does this work on Windows?**
A: Yes! Unlike browser-based tools, this API-based approach works on all platforms.

---

## API Reference

### List Accounts
```bash
python wechat_api.py list-accounts
```

### Publish Markdown Article
```bash
python wechat_api.py publish --appid <appid> --markdown /path/to/article.md
```

### Publish HTML Article
```bash
python wechat_api.py publish --appid <appid> --html /path/to/article.html
```

### Publish as 小绿书
```bash
python wechat_api.py publish --appid <appid> --markdown /path/to/article.md --type newspic
```

---

## Documentation

- [Detailed Usage Guide](docs/GUIDE.md) — Complete documentation with examples

---

## Changelog

### v1.1.0 (2025-01)
- Add HTML file support with formatting preserved
- Auto-detect file format (Markdown or HTML)
- Extract title from HTML `<title>` or `<h1>` tags
- Support inline styles and rich HTML formatting

### v1.0.0 (2025-01)
- Initial release for WeChat Official Account
- API-based publishing (no browser automation)
- Cross-platform support (macOS, Linux, Windows)
- Markdown to WeChat format conversion
- Auto image upload
- 小绿书 (newspic) support
- Draft-only publishing (safe by design)

---

## License

MIT License - see [LICENSE](LICENSE)

## Author

[iamzifei](https://github.com/iamzifei)

---

## Contributing

- **Issues**: Report bugs or request features
- **PRs**: Welcome!

---

<br><br>

---

<h1 id="中文文档">微信公众号文章发布 Skill</h1>

<p align="center">
  <a href="#wechat-article-publisher-skill">English</a> | <strong>中文</strong>
</p>

> 一键将 Markdown 或 HTML 文章发布到微信公众号草稿箱，告别繁琐的复制粘贴排版流程。

**v1.1.0** — 基于 API 的发布方式，稳定高效，支持 Markdown 和 HTML

---

## 痛点分析

如果你习惯用 Markdown 写作，将内容发布到微信公众号是一个**极其痛苦**的过程：

| 痛点 | 描述 |
|------|------|
| **格式丢失** | 从 Markdown 编辑器复制 -> 粘贴到公众号后台 -> 格式全部丢失 |
| **手动排版** | 逐个设置 H2、粗体、链接 — 每篇文章 15-20 分钟 |
| **图片上传繁琐** | 需要通过素材库逐张上传图片 |
| **步骤繁多** | 在 Markdown 编辑器、图片上传、公众号后台之间反复切换 |

### 时间对比

| 操作 | 手动方式 | 使用本 Skill |
|------|----------|--------------|
| 格式转换 | 15-20 分钟 | 0（自动） |
| 图片上传 | 5-10 分钟 | 0（自动） |
| 复制粘贴内容 | 2-3 分钟 | 0（自动） |
| **总计** | **20-30 分钟** | **< 1 分钟** |

**效率提升 30 倍以上**

---

## 解决方案

本 Skill 使用微信 API 直接发布，稳定可靠：

```
Markdown/HTML 文件
     | Python 解析
     v
结构化数据（标题、内容、图片）
     | WeChat API
     v
保存到公众号草稿箱（绝不自动发布）
```

### 核心特性

- **基于 API**：直接调用 API，无需浏览器自动化
- **跨平台**：支持 macOS、Linux、Windows
- **双格式支持**：同时支持 Markdown (.md) 和 HTML (.html) 文件
- **格式保留**：HTML 格式完整保留，Markdown 自动转换
- **图片自动上传**：文章中的图片自动上传到微信服务器
- **安全设计**：仅保存草稿，绝不自动发布
- **小绿书支持**：支持发布为图文消息格式

---

## 环境要求

| 要求 | 说明 |
|------|------|
| Claude Code | [claude.ai/code](https://claude.ai/code) |
| Python 3.9+ | 仅使用标准库，无需额外依赖 |
| WECHAT_API_KEY | 从 [wx.limyai.com](https://wx.limyai.com) 获取 |
| 微信公众号 | 在 wx.limyai.com 完成授权 |

---

## 安装方式

### 步骤一：克隆仓库

```bash
git clone https://github.com/iamzifei/wechat-article-publisher-skill.git
```

### 步骤二：复制 Skill 到 Claude

```bash
cp -r wechat-article-publisher-skill/skills/wechat-article-publisher ~/.claude/skills/
```

### 步骤三：配置 API Key

```bash
cd wechat-article-publisher-skill
cp .env.example .env
# 编辑 .env 文件，设置你的 WECHAT_API_KEY
```

---

## 使用方法

### 自然语言

```
把 /path/to/article.md 发布到微信公众号
```

```
帮我把这篇文章发到公众号：~/articles/ai-tools.md
```

```
把这个HTML文章发布到公众号：~/newsletter/issue-01.html
```

```
Publish ~/Documents/my-post.md to WeChat
```

```
发布这个带排版的HTML文件到微信：~/export/formatted-post.html
```

### Skill 命令

```
/wechat-article-publisher /path/to/article.md
```

```
/wechat-article-publisher /path/to/article.html
```

### 带选项使用

```
# 发布为小绿书（图文消息）
/wechat-article-publisher /path/to/article.md --type newspic
```

---

## 工作流程

```
[1/4] 检查 API Key...
      -> 从 .env 加载 WECHAT_API_KEY

[2/4] 获取公众号列表...
      -> 查找已授权的公众号
      -> 如果只有一个则自动选择，多个则询问用户

[3/4] 发布文章...
      -> 检测文件格式（Markdown 或 HTML）
      -> 解析内容（标题、正文、图片）
      -> 调用微信 API
      -> 自动上传图片

[4/4] 报告结果...
      -> 显示成功信息
      -> 提醒用户手动预览并发布
```

---

## 支持的格式

### Markdown (.md)

| 语法 | 效果 |
|------|------|
| `# H1` | 文章标题（提取后不含在正文中） |
| `## H2` | 二级标题 |
| `### H3` | 三级标题 |
| `**粗体**` | **粗体文字** |
| `*斜体*` | *斜体文字* |
| `[文字](url)` | 超链接 |
| `> 引用` | 引用块 |
| `- 列表` | 无序列表 |
| `1. 列表` | 有序列表 |
| ``` 代码 ``` | 代码块 |
| `![](img.jpg)` | 图片（自动上传） |

### HTML (.html)

| 元素 | 效果 |
|------|------|
| `<title>` 或 `<h1>` | 文章标题 |
| `<h2>`, `<h3>` | 章节标题 |
| `<strong>`, `<b>` | **粗体文字** |
| `<em>`, `<i>` | *斜体文字* |
| `<a href="">` | 超链接 |
| `<blockquote>` | 引用块 |
| `<ul>`, `<ol>` | 列表 |
| `<table>` | 表格（保留） |
| `<img src="">` | 图片（自动上传） |
| 内联样式 | 保留 |

---

## 文章类型

### news（默认）
标准的公众号文章格式，支持完整的富文本。

### newspic（小绿书）
以图片为主的内容格式：
- 最多支持 20 张图片
- 文字内容限制 1000 字
- 适合图片为主的内容发布

---

## 完整示例

### 输入：`article.md`

```markdown
# 2024 年最值得关注的 5 个 AI 工具

![封面](./images/cover.jpg)

人工智能工具在 2024 年迎来了爆发式增长。本文将介绍 5 个最值得关注的工具。

## 1. Claude：最强对话 AI

**Claude** 由 Anthropic 开发，在长文本理解方面表现出色。

> Claude 的上下文窗口高达 200K tokens。

![claude-demo](./images/claude-demo.png)
```

### 执行命令

```
把 ~/Documents/article.md 发布到微信公众号
```

### 执行结果

```
✓ 文章已成功发布到公众号草稿箱！

标题: 2024 年最值得关注的 5 个 AI 工具
状态: 已保存到草稿箱

请登录微信公众平台预览并发布。
```

---

## 项目结构

```
wechat-article-publisher-skill/
├── .claude-plugin/
│   └── plugin.json              # 插件配置
├── skills/
│   └── wechat-article-publisher/
│       ├── SKILL.md             # Skill 核心指令
│       └── scripts/
│           ├── wechat_api.py    # 微信 API 客户端
│           └── parse_markdown.py # Markdown 解析器
├── docs/
│   └── GUIDE.md                 # 详细使用指南
├── .env.example                 # 环境变量模板
├── README.md                    # 本文件（双语）
└── LICENSE
```

---

## 常见问题

**Q: 如何获取 WECHAT_API_KEY？**
A: 访问 [wx.limyai.com](https://wx.limyai.com)，注册并授权你的微信公众号，在控制台获取 API Key。

**Q: 可以发布到多个公众号吗？**
A: 可以！如果你授权了多个公众号，Skill 会询问你要发布到哪个。

**Q: 图片会怎么处理？**
A: 图片会自动上传到微信服务器。支持本地路径和网络 URL。

**Q: 会自动发布文章吗？**
A: 不会。文章始终保存为草稿，你需要在公众号后台手动发布。

**Q: news 和 newspic 有什么区别？**
A: `news` 是标准文章格式；`newspic`（小绿书）是图文消息格式，以图片为主，文字有限制。

**Q: 支持 Windows 吗？**
A: 支持！与浏览器自动化工具不同，本 Skill 基于 API，支持所有平台。

---

## API 参考

### 获取公众号列表
```bash
python wechat_api.py list-accounts
```

### 发布 Markdown 文章
```bash
python wechat_api.py publish --appid <appid> --markdown /path/to/article.md
```

### 发布 HTML 文章
```bash
python wechat_api.py publish --appid <appid> --html /path/to/article.html
```

### 发布为小绿书
```bash
python wechat_api.py publish --appid <appid> --markdown /path/to/article.md --type newspic
```

---

## 详细文档

- [完整使用指南](docs/GUIDE.md) — 包含详细说明和更多示例

---

## 更新日志

### v1.1.0 (2025-01)
- 新增 HTML 文件支持，保留原有格式
- 自动检测文件格式（Markdown 或 HTML）
- 从 HTML `<title>` 或 `<h1>` 标签提取标题
- 支持内联样式和丰富的 HTML 格式

### v1.0.0 (2025-01)
- 首次发布，支持微信公众号
- 基于 API 发布（无需浏览器自动化）
- 跨平台支持（macOS、Linux、Windows）
- Markdown 自动转换为公众号格式
- 图片自动上传
- 小绿书（newspic）支持
- 仅保存草稿（安全设计）

---

## 许可证

MIT License - 见 [LICENSE](LICENSE)

## 作者

[iamzifei](https://github.com/iamzifei)

---

## 贡献

- **Issues**：报告 Bug 或提出功能建议
- **PR**：欢迎贡献代码
