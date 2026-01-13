# WeChat Article Publisher Skill

[English](README.md) | [中文](README_CN.md)

> Publish Markdown articles to WeChat Official Account drafts with one command. Say goodbye to tedious copy-paste-format workflows.

**v1.0.0** — API-based publishing for reliability and speed

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
Markdown File
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
- **Format Preserved**: Markdown automatically converted to WeChat-compatible format
- **Image Auto-Upload**: Images in your markdown are automatically uploaded
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

### Skill Command

```
/wechat-article-publisher /path/to/article.md
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
      -> Parse markdown (title, content, images)
      -> Call WeChat API
      -> Upload images automatically

[4/4] Report Result...
      -> Show success message
      -> Remind to review and publish manually
```

---

## Supported Markdown

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
├── README.md                    # This file
├── README_CN.md                 # Chinese version
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

### Publish Article
```bash
python wechat_api.py publish --appid <appid> --markdown /path/to/article.md
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
