"""Topic queue management: read from queue.yaml, skip processed URLs."""
from dataclasses import dataclass, field
from pathlib import Path
import yaml

from .dedup import is_processed

_QUEUE_PATH = Path(__file__).parent.parent / "state" / "queue.yaml"


@dataclass
class Topic:
    url: str
    type: str
    priority: int = 1
    tags: list[str] = field(default_factory=list)
    notion_page_id: str | None = None


def get_next(skip_dedup: bool = False) -> Topic | None:
    """Return the highest-priority unprocessed topic from Notion or local queue."""
    # Try Notion first
    from .notion_client import NotionClient
    notion = NotionClient()
    if notion.client:
        topic = notion.fetch_next_article()
        if topic:
            return topic

    # Fallback to local queue.yaml
    if not _QUEUE_PATH.exists():
        return None

    with open(_QUEUE_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    topics = data.get("topics") or []
    if not topics:
        return None

    # Sort by priority (ascending = higher priority first)
    sorted_topics = sorted(topics, key=lambda t: t.get("priority", 99))

    for t in sorted_topics:
        url = t["url"]
        if skip_dedup or not is_processed(url):
            return Topic(
                url=url,
                type=t.get("type", "tool_explainer"),
                priority=t.get("priority", 1),
                tags=t.get("tags", []),
            )

    return None
