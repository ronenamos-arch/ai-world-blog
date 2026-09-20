#!/usr/bin/env python3
"""
End-to-end test: Generate one complete post without API calls.
Mocks Claude API, generates real markdown, updates Notion.
"""
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv

# Load environment
_ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(_ENV_PATH)


# Mock responses for Claude API
MOCK_OUTLINE = """
# GitHub for Beginners

## Key Points
- Getting started with GitHub basics
- Creating your first repository
- Understanding commits and branches
- Collaborating with others
- Best practices for open source

## Structure
Introduction → Setup → First Repo → Collaboration → Best Practices
"""

MOCK_FULL_POST = """# GitHub for Beginners: Getting Started with GitHub Pages

GitHub is the world's leading platform for version control and collaboration. Whether you're building software, managing documentation, or contributing to open source, GitHub makes it simple to work together.

## What is GitHub?

GitHub is built on Git, a distributed version control system. It allows you to:
- Track changes to your code over time
- Collaborate with teammates
- Manage different versions of your project
- Contribute to open source projects

## Getting Started

### Step 1: Create an Account
Visit github.com and sign up for a free account. Free accounts get unlimited public and private repositories.

### Step 2: Create Your First Repository
A repository (or "repo") is like a folder for your project. It contains all your project's files and the history of changes.

To create a repo:
1. Click the "+" icon in the top right
2. Select "New repository"
3. Give it a name (e.g., "my-first-project")
4. Add a description
5. Choose Public or Private
6. Click "Create repository"

### Step 3: Understanding Commits
A commit is a snapshot of your code at a specific point in time. Each commit has a message describing what changed.

Good commit messages are:
- Descriptive: "Add user authentication" not "fix stuff"
- Concise: Keep it under 50 characters for the main message
- Consistent: Use present tense ("Add" not "Added")

### Step 4: Branches and Pull Requests
Branches let you work on features without affecting the main codebase.

Typical workflow:
1. Create a branch for your feature
2. Make changes and commit
3. Create a Pull Request (PR)
4. Team reviews and discusses
5. Merge when approved

## Collaborating on GitHub

### Forking a Project
Forking creates your own copy of someone else's repository. You can:
- Experiment freely
- Make improvements
- Submit a Pull Request with your changes

### Writing Good Issues
When you find a bug or want to suggest a feature:
- Be specific about what's happening
- Include steps to reproduce
- Explain what you expected to happen
- Add relevant screenshots or logs

## Best Practices for GitHub

1. **Commit Often**: Small, focused commits are easier to review and understand
2. **Write Clear Messages**: Future you (and your team) will thank you
3. **Use Branches**: Keep experimental work separate
4. **Review Code**: Learn from others' approaches
5. **Document Your Project**: A good README helps others understand your work

## Conclusion

GitHub is an essential tool for modern development. Start with these basics and gradually explore more advanced features like Actions, Discussions, and Projects.

Happy coding!
"""

MOCK_REVIEW = {
    "score": 8,
    "word_count": 650,
    "issues": []
}


def mock_claude_calls():
    """Create patches for Claude API calls."""
    patches = []

    # Mock scrape_url
    scrape_patch = patch('src.firecrawl_client.scrape_url')
    mock_scrape = scrape_patch.start()
    mock_scrape.return_value = {
        'content_markdown': """
# GitHub for Beginners

Getting started with GitHub and GitHub Pages...
[Sample content from article]
"""
    }
    patches.append(scrape_patch)

    # Mock generate_outline
    outline_patch = patch('src.claude_client.generate_outline')
    mock_outline = outline_patch.start()
    mock_outline.return_value = MOCK_OUTLINE
    patches.append(outline_patch)

    # Mock generate_post
    post_patch = patch('src.claude_client.generate_post')
    mock_post = post_patch.start()
    mock_post.return_value = MOCK_FULL_POST
    patches.append(post_patch)

    # Mock self_review
    review_patch = patch('src.claude_client.self_review')
    mock_review_func = review_patch.start()
    mock_review_func.return_value = MOCK_REVIEW
    patches.append(review_patch)

    return patches


def test_full_generation():
    """Run a complete generation test."""
    print("=" * 70)
    print("🚀 END-TO-END TEST: Generate One Complete Post (No API Calls)")
    print("=" * 70)

    from src.notion_client import NotionClient
    from src.queue_manager import get_next

    # Get next article from Notion
    print("\n[1/6] Fetching next article from Notion...")
    topic = get_next()
    if not topic:
        print("❌ No articles in Notion queue")
        return False

    print(f"✓ Fetched: {topic.url[:60]}...")
    notion_page_id = topic.notion_page_id
    print(f"  Notion ID: {notion_page_id}")

    # Update Notion: In Progress
    print("\n[2/6] Updating Notion: In Progress...")
    notion = NotionClient()
    notion.update_status(notion_page_id, "In Progress")
    print("✓ Status updated to 'In Progress'")

    # Mock the API calls and run pipeline
    print("\n[3/6] Generating post (mocking API calls)...")
    patches = mock_claude_calls()

    try:
        from src.pipeline import run
        result = run(
            url=topic.url,
            post_type=topic.type,
            tags=topic.tags,
            dry_run=False  # Actually write the file
        )
        print("✓ Post generated successfully")
        print(f"  Slug: {result['slug']}")
        print(f"  File: {result['output_path']}")
        print(f"  Score: {result['score']}/10")
        print(f"  Words: {result['word_count']}")
    finally:
        # Stop all patches
        for p in patches:
            p.stop()

    # Update Notion: Metrics
    print("\n[4/6] Updating Notion: Metrics...")
    notion.update_generation_metrics(
        notion_page_id,
        score=result['score'],
        word_count=result['word_count'],
        slug=result['slug']
    )
    print("✓ Metrics saved to Notion:")
    print(f"  ניקוד (Score): {result['score']}/10")
    print(f"  מילים (Words): {result['word_count']}")
    print(f"  Slug: {result['slug']}")

    # Update Notion: Ready to Publish
    print("\n[5/6] Updating Notion: Ready to Publish...")
    notion.update_status(notion_page_id, "Ready to Publish")
    print("✓ Status updated to 'Ready to Publish'")

    # Show next steps
    print("\n[6/6] Next Steps (Manual)...")
    post_path = result['output_path']
    print(f"✓ Post file created: {post_path}")
    print("\n" + "=" * 70)
    print("✅ TEST COMPLETE - Post Generated Successfully!")
    print("=" * 70)

    print(f"""
📝 POST DETAILS:
   Title: Generated from article
   File: {post_path}
   Status: draft: true (needs to be changed to false)

🔔 NOTION UPDATES:
   Status: Ready to Publish ✓
   Score: {result['score']}/10 ✓
   Word count: {result['word_count']} ✓
   Slug: {result['slug']} ✓

📋 NEXT STEPS (when ready):
   1. Review the post file
   2. Change 'draft: false' in frontmatter
   3. Commit & push to GitHub
   4. Run: python -m src.cli --publish {result['slug']}
   5. Notion status will update to 'Published'

""")

    return True


if __name__ == "__main__":
    try:
        success = test_full_generation()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed:")
        print(f"  {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
