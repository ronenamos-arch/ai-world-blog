"""Hebrew → Latin slug transliteration.

Strategy:
1. Extract Latin/ASCII words from the title (tool names, brands, numbers)
2. If 2+ meaningful words found → use those (e.g. "perplexity" from "Perplexity — מנוע החיפוש")
3. Otherwise fall back to full anyascii transliteration
"""
import re
from urllib.parse import urlparse
from anyascii import anyascii
from slugify import slugify


def slug_from_url(url: str) -> str | None:
    """Extract a clean slug from a source URL path (used as fallback)."""
    try:
        path = urlparse(url).path.strip("/")
        # Take the last path segment
        segment = path.split("/")[-1]
        # Remove trailing slashes and clean up
        return slugify(segment, separator="-", lowercase=True, max_length=60) or None
    except Exception:
        return None


def make_slug(text: str, source_url: str | None = None) -> str:
    """Convert Hebrew (or mixed) text to a URL-safe Latin slug.

    Examples:
        make_slug("Perplexity — מנוע החיפוש שבאמת עונה לך")  -> "perplexity"
        make_slug("ChatGPT לעסקים קטנים")                     -> "chatgpt-lsqm-qtnym"... no, "chatgpt"
        make_slug("מה זה Claude Projects")                    -> "claude-projects"
        make_slug("10 כלים ל-AI שכדאי להכיר")                -> "10-ai"
        make_slug("השוואה: Notion מול Obsidian")              -> "notion-obsidian"
    """
    # Step 1: find all Latin-looking tokens (letters, digits, hyphens between them)
    latin_tokens = re.findall(r'[A-Za-z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)*|[0-9]+', text)

    # Filter out very short stop-words that add no meaning (a, i, or, vs, to, of...)
    stop = {'a', 'i', 'or', 'to', 'of', 'in', 'on', 'at', 'by', 'is', 'it', 'be', 'vs', 'ai', 'ml'}
    meaningful = [t for t in latin_tokens if t.lower() not in stop and (len(t) > 1 or t.isdigit())]

    # Need at least 2 meaningful tokens, or 1 token that's longer than 4 chars (a real brand name)
    if len(meaningful) >= 2 or (len(meaningful) == 1 and len(meaningful[0]) > 4):
        # Use Latin words only (e.g. brand names, tool names, numbers)
        combined = " ".join(meaningful)
        return slugify(combined, separator="-", lowercase=True)

    # Step 2: fallback — use source URL slug if available (cleaner than transliteration)
    if source_url:
        url_slug = slug_from_url(source_url)
        if url_slug:
            return url_slug

    # Step 3: last resort — transliterate everything
    ascii_text = anyascii(text)
    return slugify(ascii_text, separator="-", lowercase=True)
