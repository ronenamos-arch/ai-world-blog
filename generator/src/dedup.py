"""Deduplication: track processed URLs to avoid regenerating posts."""
import json
from datetime import datetime, timezone
from pathlib import Path

_STATE_PATH = Path(__file__).parent.parent / "state" / "processed.json"


def _load() -> dict:
    if not _STATE_PATH.exists():
        return {"processed": []}
    with open(_STATE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(data: dict) -> None:
    with open(_STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def is_processed(url: str) -> bool:
    data = _load()
    return any(entry["url"] == url for entry in data["processed"])


def mark_processed(url: str, slug: str, generated_at: datetime | None = None) -> None:
    data = _load()
    data["processed"].append({
        "url": url,
        "slug": slug,
        "generated_at": (generated_at or datetime.now(timezone.utc)).isoformat(),
    })
    _save(data)
