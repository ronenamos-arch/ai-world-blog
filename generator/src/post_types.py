"""Mapping of post types to their prompt files."""
from pathlib import Path

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"

POST_TYPES = {
    "tool_explainer": PROMPTS_DIR / "tool_explainer.md",
    "tutorial": PROMPTS_DIR / "tutorial.md",
    "comparison": PROMPTS_DIR / "comparison.md",
    "use_case": PROMPTS_DIR / "use_case.md",
}

VALID_POST_TYPES = list(POST_TYPES.keys())


def get_post_type_prompt(post_type: str) -> str:
    if post_type not in POST_TYPES:
        raise ValueError(f"Unknown post type: {post_type!r}. Valid: {VALID_POST_TYPES}")
    path = POST_TYPES[post_type]
    return path.read_text(encoding="utf-8")
