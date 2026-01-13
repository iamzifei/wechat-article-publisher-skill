# LinkedIn Article Publisher Skill

[English](README.md) | [中文](README_CN.md)

> Publish Markdown articles to LinkedIn Articles with one command. Say goodbye to tedious rich text editing.

**v1.0.0** — Block-index positioning for precise image placement

---

## The Problem

If you're used to writing in Markdown, publishing to LinkedIn Articles is a **painful process**:

| Pain Point | Description |
|------------|-------------|
| **Format Loss** | Copy from Markdown editor -> Paste to LinkedIn -> All formatting gone |
| **Manual Formatting** | Set each H2, bold, link manually — 15-20 min per article |
| **Tedious Image Upload** | Multiple clicks per image: Add media -> Select -> Wait |
| **Position Errors** | Hard to remember where each image should go |

### Time Comparison

| Task | Manual | With This Skill |
|------|--------|-----------------|
| Format conversion | 15-20 min | 0 (automatic) |
| Cover image | 1-2 min | 10 sec |
| 5 content images | 5-10 min | 1 min |
| **Total** | **20-30 min** | **2-3 min** |

**10x efficiency improvement**

---

## The Solution

This skill automates the entire publishing workflow:

```
Markdown File
     | Python parsing
     v
Structured Data (title, images with block_index, HTML)
     | Playwright MCP
     v
LinkedIn Articles Editor (browser automation)
     |
     v
Draft Saved (never auto-publishes)
```

### Key Features

- **Rich Text Paste**: Convert Markdown to HTML, paste via clipboard — all formatting preserved
- **Block-Index Positioning**: Precise image placement using element indices, not text matching
- **Reverse Insertion**: Insert images from highest to lowest index to avoid position shifts
- **Smart Wait Strategy**: Conditions return immediately when met, no wasted wait time
- **Safe by Design**: Only saves as draft, never publishes automatically

---

## Why Block-Index?

Previously, images were positioned by matching surrounding text — this failed when:
- Multiple paragraphs had similar content
- Text was too short to be unique

Now, each image has a `block_index` indicating exactly which block element it follows. This is deterministic and reliable.

---

## Requirements

| Requirement | Details |
|-------------|---------|
| Claude Code | [claude.ai/code](https://claude.ai/code) |
| Playwright MCP | Browser automation |
| LinkedIn Account | Free account works (no Premium required) |
| Python 3.9+ | With dependencies below |
| macOS | Currently macOS only |

```bash
pip install Pillow pyobjc-framework-Cocoa
```

---

## Installation

### Method 1: Git Clone (Recommended)

```bash
git clone https://github.com/iamzifei/linkedin-article-publisher-skill.git
cp -r linkedin-article-publisher-skill/skills/linkedin-article-publisher ~/.claude/skills/
```

### Method 2: Plugin Marketplace

```
/plugin marketplace add iamzifei/linkedin-article-publisher-skill
/plugin install linkedin-article-publisher@iamzifei/linkedin-article-publisher-skill
```

---

## Usage

### Natural Language

```
Publish /path/to/article.md to LinkedIn
```

```
Help me post this article to LinkedIn: ~/Documents/my-post.md
```

### Skill Command

```
/linkedin-article-publisher /path/to/article.md
```

---

## Workflow Steps

```
[1/7] Parse Markdown...
      -> Extract title, cover image, content images with block_index
      -> Convert to HTML, count total blocks

[2/7] Open LinkedIn Articles editor...
      -> Navigate to linkedin.com/article/new/

[3/7] Upload cover image...
      -> First image becomes cover

[4/7] Fill title...
      -> H1 used as title (not included in body)

[5/7] Paste article content...
      -> Rich text via clipboard
      -> All formatting preserved

[6/7] Insert content images (reverse order)...
      -> Sort by block_index descending
      -> Click block element at index -> Paste image
      -> Wait for upload (returns immediately when done)

[7/7] Save draft...
      -> Review and publish manually
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
| `![](img.jpg)` | Images (first = cover) |

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

## 2. Midjourney: AI Art Leader

[Midjourney](https://midjourney.com) is the most popular AI art tool.

![midjourney](./images/midjourney.jpg)
```

### Parsed Output (JSON)

```json
{
  "title": "5 AI Tools Worth Watching in 2024",
  "cover_image": "./images/cover.jpg",
  "content_images": [
    {"path": "./images/claude-demo.png", "block_index": 4},
    {"path": "./images/midjourney.jpg", "block_index": 6}
  ],
  "total_blocks": 7
}
```

### Insertion Order

Images inserted in reverse: `block_index=6` first, then `block_index=4`.

### Result

- Cover: `cover.jpg` uploaded
- Title: "5 AI Tools Worth Watching in 2024"
- Content: Rich text with H2, bold, quotes, links
- Images: Inserted at precise positions via block index
- Status: **Draft saved** (ready for manual review)

---

## Project Structure

```
linkedin-article-publisher-skill/
├── .claude-plugin/
│   └── plugin.json              # Plugin config
├── skills/
│   └── linkedin-article-publisher/
│       ├── SKILL.md             # Skill instructions
│       └── scripts/
│           ├── parse_markdown.py    # Extracts block_index
│           └── copy_to_clipboard.py
├── docs/
│   └── GUIDE.md                 # Detailed guide
├── README.md                    # This file
├── README_CN.md                 # Chinese version
└── LICENSE
```

---

## FAQ

**Q: Why doesn't LinkedIn require Premium?**
A: Unlike X Articles which requires Premium Plus, LinkedIn Articles is available to all users with a LinkedIn account.

**Q: Windows/Linux support?**
A: Currently macOS only. PRs welcome for cross-platform clipboard support.

**Q: Image upload failed?**
A: Check: valid path, supported format (jpg/png/gif/webp), stable network.

**Q: Can I publish to multiple accounts?**
A: Not automatically. Switch accounts in browser manually before running.

**Q: Why insert images in reverse order?**
A: Each inserted image shifts subsequent block indices. Inserting from highest to lowest ensures earlier indices remain valid.

**Q: Why does wait return immediately sometimes?**
A: `browser_wait_for time=X` returns as soon as the operation completes. The `time` parameter is just a maximum, not a fixed delay.

---

## Documentation

- [Detailed Usage Guide](docs/GUIDE.md) — Complete documentation with examples

---

## Changelog

### v1.0.0 (2025-01)
- Initial release for LinkedIn Articles
- Rich text paste via clipboard
- Block-index positioning for precise image placement
- Reverse insertion order to prevent index shifts
- Cover + content image support
- Draft-only publishing (safe by design)

---

## License

MIT License - see [LICENSE](LICENSE)

## Author

[iamzifei](https://github.com/iamzifei)

---

## Contributing

- **Issues**: Report bugs or request features
- **PRs**: Welcome! Especially for Windows/Linux support
