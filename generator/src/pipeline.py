"""Orchestrator: runs the full generation pipeline for one topic."""
from pathlib import Path

from .config import get_config
from .firecrawl_client import scrape_url
from .claude_client import generate_outline, generate_post, self_review
from .markdown_writer import write_post
from .dedup import mark_processed


def run(
    url: str,
    post_type: str,
    tags: list[str] | None = None,
    dry_run: bool = False,
) -> dict:
    """Run the full pipeline for a single URL.

    Returns:
        dict with keys: slug, output_path, score, word_count, issues
    """
    cfg = get_config()
    model = cfg["claude"]["model"]
    max_tokens = cfg["claude"]["max_tokens"]
    min_score = cfg["review"]["min_score"]

    print(f"[1/5] Scraping: {url}")
    scraped = scrape_url(url)
    source_markdown = scraped["content_markdown"]

    if not source_markdown.strip():
        raise RuntimeError(f"Firecrawl returned empty content for: {url}")

    print(f"[2/5] Generating outline ({post_type})...")
    outline = generate_outline(source_markdown, post_type, model, max_tokens)

    print(f"[3/5] Writing full post...")
    post_markdown = generate_post(outline, source_markdown, post_type, model, max_tokens)

    print(f"[4/5] Self-review...")
    review = self_review(post_markdown, model, 512)
    score = review.get("score", 0)
    word_count = review.get("word_count", 0)
    issues = review.get("issues", [])

    print(f"      Score: {score}/10 | Words: {word_count}")
    if issues:
        print(f"      Issues: {', '.join(issues)}")

    if score < min_score:
        print(f"[WARN] Score {score} below minimum {min_score}. Post saved as draft for manual review.")

    if dry_run:
        print("[5/5] DRY RUN — not writing file.")
        return {"slug": "(dry-run)", "output_path": None, "score": score, "word_count": word_count, "issues": issues}

    print(f"[5/5] Writing Markdown file...")
    output_path = write_post(post_markdown, tags=tags, draft=True)
    slug = output_path.stem

    mark_processed(url, slug)

    print(f"      Saved: {output_path}")
    return {"slug": slug, "output_path": output_path, "score": score, "word_count": word_count, "issues": issues}
