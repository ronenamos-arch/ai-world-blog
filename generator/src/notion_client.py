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
                
            # Query database for articles with "Not started" status
            # Use page_size=10 to get multiple results since some may not have URLs
            response = self.client.data_sources.query(
                data_source_id=db_id,
                filter={
                    "property": "Status",
                    "status": {
                        "equals": "Not started"
                    }
                },
                page_size=10
            )
            
            results = response.get("results")
            if not results:
                return None

            # Iterate through results to find one with a valid URL
            for page in results:
                props = page.get("properties", {})

                # Extract URL from "URL מקור"
                url_prop = props.get("URL מקור", {})
                url = url_prop.get("url")

                # Skip if no URL or if URL doesn't start with http (invalid format)
                if not url or not url.startswith(("http://", "https://")):
                    continue

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

            # No items with URLs found
            return None

        except Exception as e:
            import traceback
            logger.error(f"Error fetching from Notion: {e}")
            logger.debug(traceback.format_exc())
            print(f"DEBUG Traceback: {traceback.format_exc()}")
            return None

    def update_status(self, page_id: str, status: str):
        """Update the Status property. Gracefully handles missing status options."""
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
            logger.info(f"Updated Notion status to '{status}' for {page_id}")
        except Exception as e:
            # Log but don't fail - status may not exist in the user's database yet
            if "does not exist" in str(e).lower():
                logger.warning(f"Status '{status}' not found in Notion database. Add this status option to continue. Error: {e}")
            else:
                logger.error(f"Error updating Notion status for {page_id}: {e}")

    def update_generation_metrics(self, page_id: str, score: int, word_count: int, slug: str):
        """Update score, word count, and slug after generation."""
        if not self.client:
            return

        try:
            self.client.pages.update(
                page_id=page_id,
                properties={
                    "ניקוד": {  # Score
                        "number": score
                    },
                    "מילים": {  # Word count
                        "number": word_count
                    },
                    "Slug": {  # Slug
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": slug
                                }
                            }
                        ]
                    }
                }
            )
            logger.info(f"Updated metrics for {page_id}: score={score}, words={word_count}, slug={slug}")
        except Exception as e:
            logger.error(f"Error updating metrics for {page_id}: {e}")

    def update_blog_url(self, page_id: str, blog_url: str):
        """Update the blog post URL after publication."""
        if not self.client:
            return

        try:
            self.client.pages.update(
                page_id=page_id,
                properties={
                    "לינק לפוסט": {  # Blog post URL
                        "url": blog_url
                    }
                }
            )
            logger.info(f"Updated blog URL for {page_id}: {blog_url}")
        except Exception as e:
            logger.error(f"Error updating blog URL for {page_id}: {e}")

    def update_error(self, page_id: str, error_message: str):
        """Update status to Done (fallback if Error status doesn't exist)."""
        if not self.client:
            return

        try:
            # Try to set status to "Done" since "Error" status may not exist in the database
            # This allows the user to see which articles failed without requiring new statuses
            self.client.pages.update(
                page_id=page_id,
                properties={
                    "Status": {
                        "status": {
                            "name": "Done"
                        }
                    }
                }
            )
            logger.info(f"Updated status to Done (error occurred) for {page_id}")
        except Exception as e:
            logger.error(f"Error updating status for {page_id}: {e}")
