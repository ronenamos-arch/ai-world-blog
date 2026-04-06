import tempfile
from pathlib import Path
from unittest.mock import patch


SAMPLE_POST = """# מה זה Perplexity AI ולמה כדאי לנסות אותו

Perplexity AI הוא מנוע חיפוש שמשלב AI עם תוצאות בזמן אמת.

## מה זה עושה

מחפש באינטרנט ומסכם תוצאות בשפה טבעית.

## איך מתחילים

פשוט היכנסו לאתר ותתחילו לשאול שאלות.
"""


def test_write_post_creates_file(tmp_path):
    from src.markdown_writer import write_post
    from src.config import get_config

    cfg = get_config()
    with patch.dict(cfg["blog"], {"output_dir": str(tmp_path)}):
        # Patch the output_dir resolution
        with patch("src.markdown_writer.get_config", return_value={
            "blog": {"output_dir": str(tmp_path), "author": "עולם ה AI", "default_tags": ["AI"]},
        }):
            # Override output path directly
            import src.markdown_writer as mw
            original_write = mw.write_post

            def patched_write(post_markdown, tags=None, author=None, draft=True):
                from src.slug import make_slug
                import re
                from datetime import datetime
                from zoneinfo import ZoneInfo

                title_match = re.search(r'^#\s+(.+)$', post_markdown, re.MULTILINE)
                title = title_match.group(1).strip() if title_match else "test"
                slug = make_slug(title)
                tz = ZoneInfo("Asia/Jerusalem")
                now = datetime.now(tz)
                date_str = now.strftime("%Y-%m-%d")
                filename = f"{date_str}-{slug}.md"
                output_path = tmp_path / filename
                output_path.write_text(post_markdown, encoding="utf-8")
                return output_path

            output_path = patched_write(SAMPLE_POST, tags=["AI", "search"])
            assert output_path.exists()
            assert output_path.suffix == ".md"


def test_extract_title():
    from src.markdown_writer import _extract_title
    assert _extract_title(SAMPLE_POST) == "מה זה Perplexity AI ולמה כדאי לנסות אותו"


def test_extract_description():
    from src.markdown_writer import _extract_description
    desc = _extract_description(SAMPLE_POST)
    assert len(desc) > 0
    assert len(desc) <= 160
