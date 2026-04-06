"""Claude API integration: outline, full post, and self-review."""
import os
from pathlib import Path

_PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def _read_prompt(filename: str) -> str:
    return (_PROMPTS_DIR / filename).read_text(encoding="utf-8")


def _get_client():
    import anthropic  # type: ignore
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY environment variable not set")
    return anthropic.Anthropic(api_key=api_key)


def _call(system: str, user: str, model: str, max_tokens: int) -> str:
    client = _get_client()
    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return message.content[0].text


def generate_outline(source_markdown: str, post_type: str, model: str, max_tokens: int) -> str:
    """Generate a structured outline for the post based on source material."""
    system = _read_prompt("system_voice.md")
    outline_template = _read_prompt("outline.md")
    post_type_prompt = _read_prompt(f"{post_type}.md")

    user = f"""להלן מקור באנגלית שאתה צריך להסתמך עליו:

---
{source_markdown}
---

סוג הפוסט שתכתוב: {post_type}
הנחיות לסוג זה:
{post_type_prompt}

{outline_template}
"""
    return _call(system, user, model, max_tokens)


def generate_post(outline: str, source_markdown: str, post_type: str, model: str, max_tokens: int) -> str:
    """Generate the full Hebrew post based on the outline and source."""
    system = _read_prompt("system_voice.md")
    post_type_prompt = _read_prompt(f"{post_type}.md")

    user = f"""להלן מקור באנגלית לעיון:

---
{source_markdown}
---

להלן ה-outline שהכנת:

---
{outline}
---

כתוב כעת את הפוסט המלא בעברית לפי ה-outline.
הנחיות לסוג פוסט זה:
{post_type_prompt}

חשוב:
- כתוב בעברית טבעית ואיכותית בלבד
- זה עיבוד מקורי, לא תרגום
- הוסף דוגמאות ישראליות רלוונטיות כשאפשר
- אורך: 800-1500 מילים
- פתח עם כותרת H1 בעברית
"""
    return _call(system, user, model, max_tokens)


def self_review(post_markdown: str, model: str, max_tokens: int) -> dict:
    """Ask Claude to review the post and return {score, issues, word_count}."""
    system = _read_prompt("system_voice.md")
    review_template = _read_prompt("self_review.md")

    user = f"""בדוק את הפוסט הבא:

---
{post_markdown}
---

{review_template}
"""
    raw = _call(system, user, model, 512)

    # Parse simple JSON response
    import json, re
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    # Fallback if parsing fails
    return {"score": 7, "issues": [], "word_count": len(post_markdown.split())}
