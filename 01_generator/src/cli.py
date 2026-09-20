"""CLI entry point for the blog post generator."""
import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv

# Load .env from generator directory
_ENV_PATH = Path(__file__).parent.parent / ".env"
load_dotenv(_ENV_PATH)


def main():
    parser = argparse.ArgumentParser(
        prog="generator",
        description="Generate Hebrew AI blog posts for עולם ה AI",
    )

    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--url", help="HowDoIUseAI URL to generate a post from")
    source.add_argument("--next", action="store_true", help="Pick the next URL from queue.yaml")
    source.add_argument("--publish", help="Mark a generated post as published and update Notion with blog URL (use slug, e.g., '2026-04-14-my-post')")

    parser.add_argument(
        "--type",
        choices=["tool_explainer", "tutorial", "comparison", "use_case"],
        default="tool_explainer",
        help="Post type (default: tool_explainer)",
    )
    parser.add_argument(
        "--tags",
        nargs="+",
        help="Override tags (space-separated)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run pipeline without writing files",
    )
    parser.add_argument(
        "--no-dedup",
        action="store_true",
        help="Skip deduplication check (re-generate even if already processed)",
    )

    args = parser.parse_args()

    # Handle --publish flag
    if args.publish:
        _handle_publish(args.publish)
        return

    topic = None
    if args.next:
        from .queue_manager import get_next
        topic = get_next(skip_dedup=args.no_dedup)
        if topic is None:
            print("Queue is empty or all topics already processed.")
            sys.exit(0)
        url = topic.url
        post_type = topic.type
        tags = topic.tags or args.tags
        print(f"Next topic: {url} (type: {post_type})")
    else:
        url = args.url
        post_type = args.type
        tags = args.tags

    from .dedup import is_processed
    if not args.no_dedup and is_processed(url):
        print(f"Already processed: {url}")
        print("Use --no-dedup to force regeneration.")
        sys.exit(0)

    # Mark as "In Progress" in Notion before starting generation
    if topic and topic.notion_page_id and not args.dry_run:
        from .notion_client import NotionClient
        NotionClient().update_status(topic.notion_page_id, "In Progress")

    from .pipeline import run
    try:
        result = run(url=url, post_type=post_type, tags=tags, dry_run=args.dry_run)
    except Exception as e:
        # Update Notion with error status if generation fails
        if topic and topic.notion_page_id and not args.dry_run:
            from .notion_client import NotionClient
            NotionClient().update_error(topic.notion_page_id, str(e))
        raise

    if not args.dry_run:
        print(f"\nDone! Post saved as draft: {result['output_path']}")
        print("Edit draft: false in the frontmatter to publish.")

        if topic and topic.notion_page_id:
            from .notion_client import NotionClient
            notion = NotionClient()

            # Update metrics
            notion.update_generation_metrics(
                topic.notion_page_id,
                score=result.get('score', 0),
                word_count=result.get('word_count', 0),
                slug=result.get('slug', '')
            )

            # Set status to "Ready to Publish"
            notion.update_status(topic.notion_page_id, "Ready to Publish")
            print(f"Updated Notion entry: metrics saved, status set to Ready to Publish")


def _handle_publish(slug: str):
    """Mark a post as published and update Notion with blog URL."""
    from .notion_client import NotionClient

    print(f"Post slug: {slug}")
    notion_page_id = input("Enter the Notion page ID for this post: ").strip()
    if not notion_page_id:
        print("Skipped updating Notion.")
        return

    # Build blog URL
    blog_url = f"https://ai-world-blog.vercel.app/{slug}/"

    # Update Notion
    notion = NotionClient()
    notion.update_blog_url(notion_page_id, blog_url)
    notion.update_status(notion_page_id, "Published")

    print(f"\n✓ Updated Notion for {slug}")
    print(f"  URL: {blog_url}")
    print(f"  Status: Published")


if __name__ == "__main__":
    main()
