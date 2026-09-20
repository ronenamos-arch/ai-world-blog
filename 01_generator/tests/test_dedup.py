import json
import tempfile
from pathlib import Path
from unittest.mock import patch


def _make_dedup(tmp_path: Path):
    """Return dedup module with state pointing to tmp_path."""
    import src.dedup as dedup
    state_file = tmp_path / "processed.json"
    state_file.write_text('{"processed": []}', encoding="utf-8")
    with patch.object(dedup, "_STATE_PATH", state_file):
        yield dedup, state_file


def test_not_processed_initially(tmp_path):
    import src.dedup as dedup
    state_file = tmp_path / "processed.json"
    state_file.write_text('{"processed": []}', encoding="utf-8")
    with patch.object(dedup, "_STATE_PATH", state_file):
        assert not dedup.is_processed("https://example.com/post")


def test_mark_then_check(tmp_path):
    import src.dedup as dedup
    state_file = tmp_path / "processed.json"
    state_file.write_text('{"processed": []}', encoding="utf-8")
    url = "https://howdoiuseai.com/some-post"
    with patch.object(dedup, "_STATE_PATH", state_file):
        assert not dedup.is_processed(url)
        dedup.mark_processed(url, "some-post-slug")
        assert dedup.is_processed(url)
