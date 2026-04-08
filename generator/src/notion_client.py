import os
import logging
from typing import List, Optional
from notion_client import Client
from .queue_manager import Topic

logger = logging.getLogger(__name__)

class NotionClient:
    def __init__(self):
        self.token = os.getenv("NOTION_TOKEN")
        self.db_id = os.getenv("NOTION_DATABASE_ID")
        if not self.token or not self.db_id:
            logger.warning("NOTION_TOKEN or NOTION_DATABASE_ID not set. Notion features disabled.")
            self.client = None
        else:
            self.client = Client(auth=self.token)

    def fetch_next_article(self) -> Optional[Topic]:
        if not self.client:
            return None

        try:
            response = self.client.databases.query(
                database_id=self.db_id,
                filter={
                    "property": "Status",
                    "status": {
                        "equals": "Pending"
                    }
                },
                sorts=[
                    {
                        "property": "Priority",
                        "direction": "ascending"
                    }
                ],
                page_size=1
            )

            results = response.get("results")
            if not results:
                return None

            page = results[0]
            props = page.get("properties", {})

            # Extract URL
            url_prop = props.get("URL", {})
            url = url_prop.get("url")
            if not url:
                # Try title if URL is missing? No, URL is mandatory for our generator
                return None

            # Extract Type
            type_prop = props.get("Type", {})
            post_type = "tool_explainer"
            if type_prop.get("type") == "select":
                post_type = type_prop.get("select", {}).get("name") or "tool_explainer"

            # Extract Tags
            tags_prop = props.get("Tags", {})
            tags = []
            if tags_prop.get("type") == "multi_select":
                tags = [t["name"] for t in tags_prop.get("multi_select", [])]

            # Extract Priority
            priority_prop = props.get("Priority", {})
            priority = 1
            if priority_prop.get("type") == "number":
                priority = priority_prop.get("number") or 1

            topic = Topic(
                url=url,
                type=post_type,
                priority=priority,
                tags=tags,
                notion_page_id=page["id"]
            )
            return topic

        except Exception as e:
            logger.error(f"Error fetching from Notion: {e}")
            return None

    def update_status(self, page_id: str, status: str):
        if not self.client:
            return

        try:
            self.client.pages.update(
                page_id=page_id,
                properties={
                    "Status": {
                        "status": {
                            "name": status
                        }
                    }
                }
            )
        except Exception as e:
            logger.error(f"Error updating Notion status for {page_id}: {e}")
