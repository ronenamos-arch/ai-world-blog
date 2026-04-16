#!/usr/bin/env python3
"""
Generate all posts from Notion database with mocked Claude API.
Creates draft posts that you can review and add images to later.
"""
import os
import sys
from pathlib import Path
from unittest.mock import patch
from dotenv import load_dotenv

# Load environment
_ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(_ENV_PATH)


# Mock responses - these will be different for each post
MOCK_OUTLINES = {
    "default": """# Title

## Key Points
- Main point 1
- Main point 2
- Main point 3

## Structure
Introduction → Body → Conclusion
"""
}

MOCK_POST_TEMPLATE = """# {title}

This is a placeholder post generated with mocked content. Replace with actual content after adding images.

## Overview

This post covers the topic: {title}

## Key Sections

- Introduction
- Main content
- Best practices
- Conclusion

---

**Note:** This is a draft post. Review the content and add images before changing draft: false to publish.
"""

MOCK_REVIEW = {
    "score": 7,
    "word_count": 400,
    "issues": ["Placeholder content - requires editing"]
}


def mock_claude_calls():
    """Create patches for Claude API calls."""
    patches = []

    # Mock scrape_url
    scrape_patch = patch('src.firecrawl_client.scrape_url')
    mock_scrape = scrape_patch.start()
    mock_scrape.return_value = {
        'content_markdown': "# Article Content\nPlaceholder article from source..."
    }
    patches.append(scrape_patch)

    # Mock generate_outline
    outline_patch = patch('src.claude_client.generate_outline')
    mock_outline = outline_patch.start()
    mock_outline.return_value = MOCK_OUTLINES["default"]
    patches.append(outline_patch)

    # Mock generate_post
    post_patch = patch('src.claude_client.generate_post')
    mock_post = post_patch.start()
    def generate_post_side_effect(outline, source_markdown, post_type, model, max_tokens):
        return MOCK_POST_TEMPLATE.format(title="Generated Post", content="[Mock content]")
    mock_post.side_effect = generate_post_side_effect
    patches.append(post_patch)

    # Mock self_review
    review_patch = patch('src.claude_client.self_review')
    mock_review_func = review_patch.start()
    mock_review_func.return_value = MOCK_REVIEW
    patches.append(review_patch)

    return patches


def generate_all_posts():
    """Generate all posts from Notion queue."""
    # Mock the API calls BEFORE importing pipeline
    patches = mock_claude_calls()

    from src.notion_client import NotionClient
    from src.queue_manager import get_next
    from src.pipeline import run

    print("=" * 70)
    print("🚀 BULK POST GENERATION - ALL NOTION ITEMS")
    print("=" * 70)
    print()
    print("Mode: Mocked Claude API (no real API calls)")
    print("Posts: Will be created as DRAFT (draft: true)")
    print("Images: You'll add these manually later")
    print()
    print("=" * 70)

    post_count = 0
    successful = 0
    failed = 0

    notion = NotionClient()

    try:
        while True:
            # Get next article
            topic = get_next()
            if not topic:
                print("\n✓ Queue is empty - all posts processed!")
                break

            post_count += 1
            print(f"\n[{post_count}] Processing: {topic.url[:50]}...")

            try:
                # Update Notion: In Progress
                try:
                    notion.update_status(topic.notion_page_id, "In Progress")
                except Exception as e:
                    print(f"    ⚠️  Warning: Could not update status to 'In Progress': {str(e)}")

                # Generate post
                result = run(
                    url=topic.url,
                    post_type=topic.type,
                    tags=topic.tags,
                    dry_run=False
                )

                # Update Notion: Metrics & Ready to Publish
                try:
                    notion.update_generation_metrics(
                        topic.notion_page_id,
                        score=result.get('score', 0),
                        word_count=result.get('word_count', 0),
                        slug=result.get('slug', '')
                    )
                    notion.update_status(topic.notion_page_id, "Ready to Publish")
                except Exception as e:
                    print(f"    ⚠️  Warning: Could not update metrics in Notion: {str(e)}")

                print(f"    ✓ Generated: {result['slug']}")
                print(f"    📊 Score: {result['score']}/10 | Words: {result['word_count']}")
                successful += 1

            except Exception as e:
                print(f"    ✗ Error: {type(e).__name__}")
                try:
                    notion.update_error(topic.notion_page_id, str(e))
                except Exception as e2:
                    print(f"    ⚠️  Warning: Could not update error status in Notion: {str(e2)}")

    finally:
        # Stop all patches
        for p in patches:
            p.stop()

    # Print summary
    print("\n" + "=" * 70)
    print("📊 GENERATION COMPLETE")
    print("=" * 70)
    print(f"Total processed:  {post_count}")
    print(f"Successful:       {successful}")
    print(f"Failed:           {failed}")
    print()
    print("📝 Next Steps:")
    print("   1. Review generated posts in: blog/src/data/blog/")
    print("   2. Add images for each post")
    print("   3. Change draft: true → draft: false when ready")
    print("   4. Commit & push to deploy")
    print()
    print("🔗 Posts are marked as 'Ready to Publish' in Notion")


if __name__ == "__main__":
    try:
        generate_all_posts()
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n\n⚠️ Generation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
