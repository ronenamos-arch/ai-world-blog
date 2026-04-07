"""Unsplash image search — finds a relevant free image for each post."""
import hashlib
import json
import os
import urllib.parse
import urllib.request
from pathlib import Path

_CACHE_DIR = Path(__file__).parent.parent / ".cache" / "images"
_BLOG_IMAGES_DIR = (
    Path(__file__).parent.parent.parent / "blog" / "public" / "images" / "posts"
)

_TAG_QUERIES = {
    "אוטומציה": "workflow automation productivity",
    "חיפוש": "search engine technology",
    "כלים": "digital tools technology",
    "AI": "artificial intelligence technology",
    "כתיבה": "writing content creation",
    "עיצוב": "design creativity",
    "וידאו": "video production",
    "שיווק": "marketing digital",
    "פרודקטיביות": "productivity workspace",
    "קוד": "coding programming",
}

_DEFAULT_QUERY = "artificial intelligence technology"


def _query_from_tags(tags: list[str], title: str) -> str:
    for tag in tags:
        if tag in _TAG_QUERIES:
            return _TAG_QUERIES[tag]
    import re
    latin = re.findall(r'[A-Za-z]{3,}', title)
    if latin:
        return " ".join(latin[:3])
    return _DEFAULT_QUERY


def _cache_key(query: str) -> str:
    return hashlib.sha256(query.encode()).hexdigest()[:12]


def fetch_image(tags: list[str], title: str, slug: str, force: bool = False) -> str | None:
    """Search Unsplash, download image, save to blog/public/images/posts/.

    Returns the public path for frontmatter (e.g. /images/posts/perplexity.jpg)
    or None if unavailable.
    """
    api_key = os.environ.get("UNSPLASH_ACCESS_KEY")
    if not api_key:
        print("[image] UNSPLASH_ACCESS_KEY not set — skipping image")
        return None

    query = _query_from_tags(tags or [], title)
    cache_file = _CACHE_DIR / f"{_cache_key(query)}.json"

    if not force and cache_file.exists():
        with open(cache_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        image_url = data["url"]
        photographer = data["photographer"]
    else:
        try:
            api_url = (
                "https://api.unsplash.com/photos/random"
                f"?query={urllib.parse.quote(query)}"
                "&orientation=landscape"
                "&content_filter=high"
            )
            req = urllib.request.Request(
                api_url,
                headers={"Authorization": f"Client-ID {api_key}", "Accept-Version": "v1"},
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read())

            image_url = result["urls"]["regular"]
            photographer = result["user"]["name"]

            _CACHE_DIR.mkdir(parents=True, exist_ok=True)
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump({"url": image_url, "photographer": photographer, "query": query}, f)

        except Exception as e:
            print(f"[image] Unsplash request failed: {e}")
            return None

    _BLOG_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{slug}.jpg"
    dest = _BLOG_IMAGES_DIR / filename

    if not dest.exists() or force:
        try:
            urllib.request.urlretrieve(image_url, dest)
            print(f"[image] Saved: {filename} (📷 {photographer})")
        except Exception as e:
            print(f"[image] Download failed: {e}")
            return None

    return f"/images/posts/{filename}"
