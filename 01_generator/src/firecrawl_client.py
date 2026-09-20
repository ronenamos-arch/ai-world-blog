"""Firecrawl integration: scrape URLs and cache results locally."""
import hashlib
import json
import os
from pathlib import Path

_CACHE_DIR = Path(__file__).parent.parent / ".cache" / "scraped"


def _cache_path(url: str) -> Path:
    url_hash = hashlib.sha256(url.encode()).hexdigest()[:16]
    return _CACHE_DIR / f"{url_hash}.json"


def scrape_url(url: str, force: bool = False) -> dict:
    """Scrape a URL and return {title, content_markdown, metadata}.

    Results are cached locally to avoid repeated API calls.
    """
    cache_file = _cache_path(url)

    if not force and cache_file.exists():
        with open(cache_file, "r", encoding="utf-8") as f:
            return json.load(f)

    from firecrawl import FirecrawlApp  # type: ignore

    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        raise RuntimeError("FIRECRAWL_API_KEY environment variable not set")

    app = FirecrawlApp(api_key=api_key)
    result = app.scrape(
        url,
        formats=["markdown"],
    )

    title = (result.metadata.title if result.metadata else "") or ""
    content_markdown = result.markdown or ""
    metadata = result.metadata.model_dump() if result.metadata else {}

    data = {
        "url": url,
        "title": title,
        "content_markdown": content_markdown,
        "metadata": metadata,
    }

    _CACHE_DIR.mkdir(parents=True, exist_ok=True)
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return data
