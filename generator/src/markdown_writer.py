"""Write generated posts as Markdown files with YAML frontmatter."""
import re
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from .config import get_config
from .slug import make_slug


def _extract_title(post_markdown: str) -> str:
    """Extract the first H1 heading from the post."""
    match = re.search(r'^#\s+(.+)$', post_markdown, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return "פוסט חדש"


def _extract_description(post_markdown: str) -> str:
    """Extract the first non-heading paragraph as description."""
    lines = post_markdown.split('\n')
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#') and not line.startswith('---'):
            # Trim to ~160 chars for SEO
            return line[:160]
    return ""


def _strip_h1(post_markdown: str) -> str:
    """Remove the H1 title from the markdown body (it goes in frontmatter)."""
    return re.sub(r'^#\s+.+\n?', '', post_markdown, count=1, flags=re.MULTILINE).lstrip()


def write_post(
    post_markdown: str,
    tags: list[str] | None = None,
    author: str | None = None,
    draft: bool = True,
) -> Path:
    """Write the post to blog/src/data/blog/ and return the file path."""
    cfg = get_config()

    title = _extract_title(post_markdown)
    description = _extract_description(post_markdown)
    slug = make_slug(title)
    body = _strip_h1(post_markdown)

    tz = ZoneInfo("Asia/Jerusalem")
    now = datetime.now(tz)
    date_str = now.strftime("%Y-%m-%d")
    pub_datetime = now.strftime("%Y-%m-%dT%H:%M:%S%z")
    # Insert colon in timezone offset: +0300 -> +03:00
    pub_datetime = pub_datetime[:-2] + ":" + pub_datetime[-2:]

    final_tags = tags or cfg["blog"].get("default_tags", ["AI"])
    final_author = author or cfg["blog"]["author"]
    filename = f"{date_str}-{slug}.md"

    output_dir = Path(__file__).parent.parent / cfg["blog"]["output_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / filename

    frontmatter = f"""---
title: "{title}"
description: "{description}"
pubDatetime: {pub_datetime}
author: {final_author}
tags:
{chr(10).join(f'  - {tag}' for tag in final_tags)}
featured: false
draft: {'true' if draft else 'false'}
---

"""
    output_path.write_text(frontmatter + body, encoding="utf-8")
    return output_path
