"""Hebrew → Latin slug transliteration.

Strategy:
1. Extract Latin/ASCII words from the title (tool names, brands, numbers)
2. If 2+ meaningful words found → use those (e.g. "perplexity" from "Perplexity — מנוע החיפוש")
3. Otherwise fall back to full anyascii transliteration
"""
import re
from anyascii import anyascii
from slugify import slugify


def make_slug(text: str) -> str:
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
    stop = {'a', 'i', 'or', 'to', 'of', 'in', 'on', 'at', 'by', 'is', 'it', 'be', 'vs'}
    meaningful = [t for t in latin_tokens if t.lower() not in stop and len(t) > 1]

    if len(meaningful) >= 1:
        # Use Latin words only (e.g. brand names, tool names, numbers)
        combined = " ".join(meaningful)
        return slugify(combined, separator="-", lowercase=True)

    # Step 2: fallback — transliterate everything
    ascii_text = anyascii(text)
    return slugify(ascii_text, separator="-", lowercase=True)
