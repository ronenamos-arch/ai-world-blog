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

    from .pipeline import run
    result = run(url=url, post_type=post_type, tags=tags, dry_run=args.dry_run)

    if not args.dry_run:
        print(f"\nDone! Post saved as draft: {result['output_path']}")
        print("Edit draft: false in the frontmatter to publish.")


if __name__ == "__main__":
    main()
