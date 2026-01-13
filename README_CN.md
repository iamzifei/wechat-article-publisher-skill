# 微信公众号文章发布 Skill

[English](README.md) | [中文](README_CN.md)

> 一键将 Markdown 文章发布到微信公众号草稿箱，告别繁琐的复制粘贴排版流程。

**v1.0.0** — 基于 API 的发布方式，稳定高效

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
Markdown 文件
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
- **格式保留**：Markdown 自动转换为公众号兼容格式
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
Publish ~/Documents/my-post.md to WeChat
```

### Skill 命令

```
/wechat-article-publisher /path/to/article.md
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
      -> 解析 Markdown（标题、内容、图片）
      -> 调用微信 API
      -> 自动上传图片

[4/4] 报告结果...
      -> 显示成功信息
      -> 提醒用户手动预览并发布
```

---

## 支持的 Markdown 格式

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
├── README.md                    # 英文说明
├── README_CN.md                 # 中文说明（本文件）
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

### 发布文章
```bash
python wechat_api.py publish --appid <appid> --markdown /path/to/article.md
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
