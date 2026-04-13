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
            # Ensure ID has dashes if it's missing them
            db_id = self.db_id
            if "-" not in db_id:
                db_id = f"{db_id[:8]}-{db_id[8:12]}-{db_id[12:16]}-{db_id[16:20]}-{db_id[20:]}"
                
            # Use data_sources.query for version 3.0.0 compat
            # We filter for "Not started" as the initial status
            response = self.client.data_sources.query(
                data_source_id=db_id,
                filter={
                    "property": "Status",
                    "status": {
                        "equals": "Not started"
                    }
                },
                page_size=1
            )
            
            results = response.get("results")
            if not results:
                return None

            page = results[0]
            props = page.get("properties", {})

            # Extract URL from "URL מקור"
            url_prop = props.get("URL מקור", {})
            url = url_prop.get("url")
            if not url:
                return None

            # Extract Tags from "קטגוריה"
            tags_prop = props.get("קטגוריה", {})
            tags = []
            if tags_prop.get("type") == "multi_select":
                tags = [t["name"] for t in tags_prop.get("multi_select", [])]

            topic = Topic(
                url=url,
                type="tool_explainer",
                priority=1,
                tags=tags,
                notion_page_id=page["id"]
            )
            return topic

        except Exception as e:
            import traceback
            logger.error(f"Error fetching from Notion: {e}")
            logger.debug(traceback.format_exc())
            print(f"DEBUG Traceback: {traceback.format_exc()}")
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
