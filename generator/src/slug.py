"""Hebrew → Latin slug transliteration."""
import re
from anyascii import anyascii
from slugify import slugify


def make_slug(text: str) -> str:
    """Convert Hebrew (or mixed) text to a URL-safe Latin slug.

    Examples:
        make_slug("מה זה Claude Projects") -> "ma-ze-claude-projects"
        make_slug("10 כלים ל-AI") -> "10-klim-l-ai"
    """
    # Transliterate Hebrew characters to ASCII approximations
    ascii_text = anyascii(text)
    # Use python-slugify to normalize (lowercase, hyphens, strip punctuation)
    return slugify(ascii_text, separator="-", lowercase=True)
