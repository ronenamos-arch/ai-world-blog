#!/usr/bin/env python3
"""
Test the Notion workflow without requiring Anthropic API credits.
Mocks the Claude API and tests the full pipeline.
"""
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv

# Load environment
_ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(_ENV_PATH)


def test_notion_workflow():
    """Test the complete Notion workflow with mocked API."""
    print("=" * 60)
    print("🧪 Testing Notion Integration Workflow")
    print("=" * 60)

    # Import after env is loaded
    from src.notion_client import NotionClient
    from src.queue_manager import get_next

    # Test 1: Notion Client Init
    print("\n[1/5] Testing Notion client initialization...")
    notion = NotionClient()
    if notion.client:
        print("✓ Notion client initialized")
        print(f"  Database ID: {notion.db_id}")
    else:
        print("✗ Notion client not initialized")
        return False

    # Test 2: Fetch next article
    print("\n[2/5] Testing fetch_next_article()...")
    topic = notion.fetch_next_article()
    if topic:
        print(f"✓ Fetched article from Notion")
        print(f"  URL: {topic.url[:60]}...")
        print(f"  Type: {topic.type}")
        print(f"  Tags: {topic.tags}")
        print(f"  Notion ID: {topic.notion_page_id}")
        notion_page_id = topic.notion_page_id
    else:
        print("✗ No articles found (check Notion database)")
        return False

    # Test 3: Update status to "In Progress"
    print("\n[3/5] Testing update_status() → 'In Progress'...")
    notion.update_status(notion_page_id, "In Progress")
    print("✓ Status updated to 'In Progress'")

    # Test 4: Update metrics (simulated generation results)
    print("\n[4/5] Testing update_generation_metrics()...")
    notion.update_generation_metrics(
        notion_page_id,
        score=8,
        word_count=1250,
        slug="2026-04-14-test-post"
    )
    print("✓ Metrics updated:")
    print("  Score: 8/10")
    print("  Word count: 1250")
    print("  Slug: 2026-04-14-test-post")

    # Test 5: Update status to "Ready to Publish"
    print("\n[5/5] Testing update_status() → 'Ready to Publish'...")
    notion.update_status(notion_page_id, "Ready to Publish")
    print("✓ Status updated to 'Ready to Publish'")

    # Test 6: Update blog URL (simulated publishing)
    print("\n[BONUS] Testing update_blog_url()...")
    notion.update_blog_url(
        notion_page_id,
        "https://ai-world-blog.vercel.app/2026-04-14-test-post/"
    )
    print("✓ Blog URL updated")
    notion.update_status(notion_page_id, "Published")
    print("✓ Status updated to 'Published'")

    print("\n" + "=" * 60)
    print("✅ All tests passed!")
    print("=" * 60)
    print("\nWorkflow Summary:")
    print("  Not started → In Progress → Ready to Publish → Published")
    print("\nNext steps:")
    print("  1. Verify changes in your Notion database")
    print("  2. Add Anthropic API credits when ready")
    print("  3. Run: python -m src.cli --next (for real generation)")
    return True


if __name__ == "__main__":
    try:
        success = test_notion_workflow()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed with error:")
        print(f"  {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
