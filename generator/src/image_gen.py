"""WaveSpeed AI image generation — creates a unique image per post using Flux."""
import os
import re
import urllib.request
from pathlib import Path

_BLOG_IMAGES_DIR = (
    Path(__file__).parent.parent.parent / "blog" / "public" / "images" / "posts"
)

_TAG_TOPICS = {
    "אוטומציה": "digital automation workflow, connected data streams",
    "חיפוש": "AI search engine, glowing search interface",
    "כלים": "AI software tools, digital workspace",
    "AI": "artificial intelligence, neural network visualization",
    "כתיבה": "AI writing assistant, glowing text editor",
    "עיצוב": "AI design tools, creative digital interface",
    "וידאו": "AI video generation, cinematic digital art",
    "שיווק": "digital marketing analytics, data visualization",
    "פרודקטיביות": "productivity tools, clean digital workspace",
    "קוד": "AI coding assistant, code on dark screen",
    "Claude": "AI language model, conversational interface",
    "ChatGPT": "AI chatbot interface, glowing conversation",
    "Perplexity": "AI search engine, knowledge graph",
    "Gemini": "Google AI model, multimodal interface",
}

_DEFAULT_TOPIC = "artificial intelligence technology, futuristic digital interface"

_STYLE_SUFFIX = (
    ", professional blog header, dark indigo and purple color scheme, "
    "cinematic lighting, ultra high quality, no text, no letters, 16:9"
)


def _build_prompt(tags: list[str], title: str) -> str:
    # Check tag mapping first
    for tag in (tags or []):
        if tag in _TAG_TOPICS:
            return _TAG_TOPICS[tag] + _STYLE_SUFFIX

    # Extract English product/tool names from title (capitalized words)
    proper_nouns = re.findall(r'\b[A-Z][a-z]{2,}\b', title)
    if proper_nouns:
        tool_name = proper_nouns[0]
        return f"{tool_name} AI tool interface, futuristic digital dashboard" + _STYLE_SUFFIX

    return _DEFAULT_TOPIC + _STYLE_SUFFIX


def generate_image(tags: list[str], title: str, slug: str, force: bool = False) -> str | None:
    """Generate an image with WaveSpeed Flux, save to blog/public/images/posts/.

    Returns the public path for frontmatter (e.g. /images/posts/perplexity.jpg)
    or None if unavailable.
    """
    api_key = os.environ.get("WAVESPEED_API_KEY")
    if not api_key:
        print("[image] WAVESPEED_API_KEY not set — skipping image")
        return None

    _BLOG_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{slug}.jpg"
    dest = _BLOG_IMAGES_DIR / filename

    if dest.exists() and not force:
        print(f"[image] Using cached: {filename}")
        return f"/images/posts/{filename}"

    prompt = _build_prompt(tags, title)
    print(f"[image] Generating: {prompt[:80]}...")

    try:
        import json
        import urllib.error

        api_url = "https://api.wavespeed.ai/api/v3/wavespeed-ai/flux-schnell"
        payload = json.dumps({
            "prompt": prompt,
            "enable_sync_mode": True,
            "size": "1024x576",
            "num_inference_steps": 4,
        }).encode()

        req = urllib.request.Request(
            api_url,
            data=payload,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())

        outputs = result.get("data", {}).get("outputs", [])
        if not outputs:
            print(f"[image] No outputs in response: {result}")
            return None

        image_url = outputs[0]
        urllib.request.urlretrieve(image_url, dest)
        print(f"[image] Saved: {filename}")
        return f"/images/posts/{filename}"

    except Exception as e:
        print(f"[image] WaveSpeed request failed: {e}")
        return None
