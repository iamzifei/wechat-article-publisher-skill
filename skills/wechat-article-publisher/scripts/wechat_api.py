#!/usr/bin/env python3
"""
WeChat Official Account API client for publishing articles.

This script provides functions to interact with the WeChat API:
- List authorized WeChat official accounts
- Publish articles to WeChat drafts

Authentication:
    The API key is read from the WECHAT_API_KEY environment variable.
    You can set it in a .env file in the project root.

Usage:
    # List accounts
    python wechat_api.py list-accounts

    # Publish article
    python wechat_api.py publish --appid <wechat_appid> --title "Title" --content "Content"

    # Publish from markdown file
    python wechat_api.py publish --appid <wechat_appid> --markdown /path/to/article.md

    # Publish from HTML file (with formatting preserved)
    python wechat_api.py publish --appid <wechat_appid> --html /path/to/article.html

    # Publish as "小绿书" (image-text mode)
    python wechat_api.py publish --appid <wechat_appid> --markdown /path/to/article.md --type newspic

API Documentation:
    Base URL: https://wx.limyai.com/api/openapi
    Authentication: X-API-Key header
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# API configuration
API_BASE_URL = "https://wx.limyai.com/api/openapi"


def load_env_file(env_path: Optional[str] = None) -> None:
    """
    Load environment variables from .env file.

    Args:
        env_path: Optional path to .env file. If not provided, searches in
                  current directory and parent directories.
    """
    if env_path:
        env_file = Path(env_path)
    else:
        # Search for .env file in current and parent directories
        current = Path.cwd()
        env_file = None
        for _ in range(5):  # Search up to 5 levels
            candidate = current / ".env"
            if candidate.exists():
                env_file = candidate
                break
            current = current.parent

    if env_file and env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if key and value:
                        os.environ.setdefault(key, value)


def get_api_key() -> str:
    """
    Get the WeChat API key from environment variable.

    Returns:
        The API key string.

    Raises:
        SystemExit: If API key is not found.
    """
    # Try to load from .env file first
    load_env_file()

    api_key = os.environ.get("WECHAT_API_KEY")
    if not api_key:
        print("Error: WECHAT_API_KEY environment variable not set.", file=sys.stderr)
        print("Please set it in your .env file or environment.", file=sys.stderr)
        sys.exit(1)
    return api_key


def make_api_request(endpoint: str, data: Optional[dict] = None) -> dict:
    """
    Make a POST request to the WeChat API.

    Args:
        endpoint: API endpoint path (e.g., '/wechat-accounts')
        data: Optional JSON data to send in request body

    Returns:
        JSON response as dictionary

    Raises:
        SystemExit: On API errors
    """
    url = f"{API_BASE_URL}{endpoint}"
    api_key = get_api_key()

    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json",
    }

    body = json.dumps(data).encode("utf-8") if data else b"{}"

    try:
        request = Request(url, data=body, headers=headers, method="POST")
        with urlopen(request, timeout=60) as response:
            response_data = json.loads(response.read().decode("utf-8"))
            return response_data
    except HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        try:
            error_json = json.loads(error_body)
            error_msg = error_json.get("error", error_body)
            error_code = error_json.get("code", "UNKNOWN")
            print(f"API Error ({error_code}): {error_msg}", file=sys.stderr)
        except json.JSONDecodeError:
            print(f"HTTP Error {e.code}: {error_body or e.reason}", file=sys.stderr)
        sys.exit(1)
    except URLError as e:
        print(f"Network Error: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def list_accounts() -> dict:
    """
    Get list of authorized WeChat official accounts.

    Returns:
        API response containing accounts list

    Response format:
        {
            "success": true,
            "data": {
                "accounts": [
                    {
                        "name": "公众号名称",
                        "wechatAppid": "wx1234567890",
                        "username": "gh_abc123",
                        "avatar": "https://...",
                        "type": "subscription",
                        "verified": true,
                        "status": "active",
                        "lastAuthTime": "2024-01-01T00:00:00.000Z",
                        "createdAt": "2024-01-01T00:00:00.000Z"
                    }
                ],
                "total": 1
            }
        }
    """
    return make_api_request("/wechat-accounts")


def publish_article(
    wechat_appid: str,
    title: str,
    content: str,
    summary: Optional[str] = None,
    cover_image: Optional[str] = None,
    author: Optional[str] = None,
    content_format: str = "markdown",
    article_type: str = "news",
) -> dict:
    """
    Publish an article to WeChat official account drafts.

    Args:
        wechat_appid: WeChat AppID of the target account
        title: Article title (max 64 characters)
        content: Article content (Markdown or HTML)
        summary: Article summary (max 120 characters, optional)
        cover_image: Cover image URL (optional)
        author: Author name (optional)
        content_format: Content format - 'markdown' (default) or 'html'
        article_type: Article type - 'news' (default) or 'newspic' (小绿书)

    Returns:
        API response containing publication result

    Response format (success):
        {
            "success": true,
            "data": {
                "publicationId": "uuid-here",
                "materialId": "uuid-here",
                "mediaId": "wechat-media-id",
                "status": "published",
                "message": "文章已成功发布到公众号草稿箱"
            }
        }

    Response format (failure):
        {
            "success": false,
            "error": "错误信息",
            "code": "ERROR_CODE"
        }
    """
    data = {
        "wechatAppid": wechat_appid,
        "title": title,
        "content": content,
        "contentFormat": content_format,
        "articleType": article_type,
    }

    if summary:
        data["summary"] = summary
    if cover_image:
        data["coverImage"] = cover_image
    if author:
        data["author"] = author

    return make_api_request("/wechat-publish", data)


def parse_markdown_for_wechat(filepath: str) -> dict:
    """
    Parse a markdown file and extract data for WeChat publishing.

    Args:
        filepath: Path to the markdown file

    Returns:
        Dictionary containing:
            - title: Article title
            - content: Article content (markdown)
            - cover_image: First image URL/path (if any)
            - summary: First paragraph as summary (truncated to 120 chars)
    """
    path = Path(filepath)
    if not path.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract title from H1
    title = "Untitled"
    lines = content.strip().split("\n")
    content_start = 0

    for idx, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("# "):
            title = stripped[2:].strip()
            content_start = idx + 1
            break
        elif stripped.startswith("## "):
            title = stripped[3:].strip()
            break
        elif not stripped.startswith("!["):
            title = stripped[:64]
            break

    # Get content without H1 title
    content_lines = lines[content_start:]
    markdown_content = "\n".join(content_lines).strip()

    # Extract first image as cover
    import re
    cover_image = None
    img_pattern = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
    img_match = img_pattern.search(markdown_content)
    if img_match:
        cover_image = img_match.group(1)
        # If relative path, make absolute
        if cover_image and not cover_image.startswith(("http://", "https://")):
            cover_path = path.parent / cover_image
            if cover_path.exists():
                cover_image = str(cover_path.absolute())

    # Extract summary from first paragraph
    summary = None
    for line in content_lines:
        stripped = line.strip()
        if stripped and not stripped.startswith(("#", "!", ">", "-", "*", "`")):
            summary = stripped[:120]
            break

    return {
        "title": title,
        "content": markdown_content,
        "cover_image": cover_image,
        "summary": summary,
        "source_file": str(path.absolute()),
    }


def parse_html_for_wechat(filepath: str) -> dict:
    """
    Parse an HTML file and extract data for WeChat publishing.

    Extracts title from <title> tag, <h1> tag, or first heading.
    Uses <body> content or full content if no body tag.

    Args:
        filepath: Path to the HTML file

    Returns:
        Dictionary containing:
            - title: Article title
            - content: Article content (HTML)
            - cover_image: First image URL/path (if any)
            - summary: Text from first paragraph (truncated to 120 chars)
    """
    import re

    path = Path(filepath)
    if not path.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract title from <title> tag first
    title = "Untitled"
    title_match = re.search(r"<title[^>]*>([^<]+)</title>", content, re.IGNORECASE)
    if title_match:
        title = title_match.group(1).strip()
    else:
        # Try <h1> tag
        h1_match = re.search(r"<h1[^>]*>([^<]+)</h1>", content, re.IGNORECASE)
        if h1_match:
            title = h1_match.group(1).strip()

    # Truncate title to 64 characters (WeChat limit)
    title = title[:64]

    # Extract body content if present
    body_match = re.search(r"<body[^>]*>(.*?)</body>", content, re.IGNORECASE | re.DOTALL)
    if body_match:
        html_content = body_match.group(1).strip()
    else:
        # Use full content, but try to remove html/head tags
        html_content = re.sub(r"<html[^>]*>|</html>", "", content, flags=re.IGNORECASE)
        html_content = re.sub(r"<head[^>]*>.*?</head>", "", html_content, flags=re.IGNORECASE | re.DOTALL)
        html_content = re.sub(r"<!DOCTYPE[^>]*>", "", html_content, flags=re.IGNORECASE)
        html_content = html_content.strip()

    # Extract first image as cover
    cover_image = None
    img_match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', html_content, re.IGNORECASE)
    if img_match:
        cover_image = img_match.group(1)
        # If relative path, make absolute
        if cover_image and not cover_image.startswith(("http://", "https://", "data:")):
            cover_path = path.parent / cover_image
            if cover_path.exists():
                cover_image = str(cover_path.absolute())

    # Extract summary from first <p> tag
    summary = None
    p_match = re.search(r"<p[^>]*>([^<]+)", html_content, re.IGNORECASE)
    if p_match:
        # Remove HTML tags and get plain text
        summary_text = re.sub(r"<[^>]+>", "", p_match.group(1))
        summary = summary_text.strip()[:120]

    return {
        "title": title,
        "content": html_content,
        "cover_image": cover_image,
        "summary": summary,
        "source_file": str(path.absolute()),
    }


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="WeChat Official Account API Client"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # List accounts command
    list_parser = subparsers.add_parser(
        "list-accounts",
        help="List authorized WeChat official accounts"
    )

    # Publish command
    publish_parser = subparsers.add_parser(
        "publish",
        help="Publish article to WeChat drafts"
    )
    publish_parser.add_argument(
        "--appid",
        required=True,
        help="WeChat AppID of target account"
    )
    publish_parser.add_argument(
        "--title",
        help="Article title (max 64 characters)"
    )
    publish_parser.add_argument(
        "--content",
        help="Article content (Markdown or HTML)"
    )
    publish_parser.add_argument(
        "--markdown",
        help="Path to markdown file (alternative to --title and --content)"
    )
    publish_parser.add_argument(
        "--html",
        help="Path to HTML file (alternative to --markdown, auto-sets format to html)"
    )
    publish_parser.add_argument(
        "--summary",
        help="Article summary (max 120 characters)"
    )
    publish_parser.add_argument(
        "--cover",
        help="Cover image URL"
    )
    publish_parser.add_argument(
        "--author",
        help="Author name"
    )
    publish_parser.add_argument(
        "--format",
        choices=["markdown", "html"],
        default="markdown",
        help="Content format (default: markdown)"
    )
    publish_parser.add_argument(
        "--type",
        choices=["news", "newspic"],
        default="news",
        help="Article type: news (default) or newspic (小绿书)"
    )

    args = parser.parse_args()

    if args.command == "list-accounts":
        result = list_accounts()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == "publish":
        # Determine content format based on input
        content_format = args.format

        # Get content from file or direct input
        if args.html:
            # HTML file takes precedence, auto-set format to html
            parsed = parse_html_for_wechat(args.html)
            title = args.title or parsed["title"]
            content = parsed["content"]
            summary = args.summary or parsed["summary"]
            cover = args.cover or parsed["cover_image"]
            content_format = "html"  # Always use html format for HTML files
        elif args.markdown:
            parsed = parse_markdown_for_wechat(args.markdown)
            title = args.title or parsed["title"]
            content = parsed["content"]
            summary = args.summary or parsed["summary"]
            cover = args.cover or parsed["cover_image"]
        else:
            if not args.title or not args.content:
                print(
                    "Error: Either --markdown, --html, or both --title and --content required",
                    file=sys.stderr
                )
                sys.exit(1)
            title = args.title
            content = args.content
            summary = args.summary
            cover = args.cover

        result = publish_article(
            wechat_appid=args.appid,
            title=title,
            content=content,
            summary=summary,
            cover_image=cover,
            author=args.author,
            content_format=content_format,
            article_type=args.type,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
