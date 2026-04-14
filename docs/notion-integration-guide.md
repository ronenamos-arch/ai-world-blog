# Notion Integration Guide

Your blog generator is now fully integrated with Notion. This guide explains the new workflow and how to use it.

## New Workflow

```
Notion Database (Not started)
       ↓
[In Progress] ← Generator starts
       ↓
Generate & Score Content
       ↓
[Ready to Publish] ← Save: score, word count, slug
       ↓
Manual: Edit draft → false to publish
       ↓
Run: python -m src.cli --publish <slug>
       ↓
[Published] ← Save: blog URL
```

## Notion Database Fields

Make sure your Notion database has these fields:

| Field | Type | Purpose |
|-------|------|---------|
| Name | Title | Post title |
| URL מקור | URL | Source article URL |
| Status | Status | Workflow status (see below) |
| קטגוריה | Multi-select | Post categories/tags |
| ניקוד | Number | Review score (0-10) |
| מילים | Number | Word count |
| Slug | Text | Generated post slug |
| לינק לפוסט | URL | Published blog post URL |

### Status Values

- **Not started** — Waiting to be processed
- **In Progress** — Generator is currently processing this article
- **Ready to Publish** — Post generated, ready to edit and publish
- **Published** — Post is live on the blog
- **Error** — Generation failed (check logs for details)

## Using the Generator

### 1. Generate Next Post from Notion

```bash
cd generator
python -m src.cli --next
```

This will:
- Fetch the next "Not started" item from your Notion database
- Set status to "In Progress"
- Generate the blog post
- Save metrics (score, word count, slug) to Notion
- Set status to "Ready to Publish"

### 2. Edit and Publish

⚠️ **CRITICAL:** All generated posts start with `draft: true` and will NOT appear on the blog.

Open `blog/src/data/blog/YYYY-MM-DD-slug.md`:
- Review the content
- **Change `draft: true` → `draft: false`** ← THIS IS ESSENTIAL
- Commit and push to trigger Vercel deployment

**Without this step, your post will deploy but not appear on the blog.**

See: [Deployment Checklist](./deployment-checklist.md) for detailed steps.

### 3. Update Notion with Published Link

After the blog post is published:

```bash
python -m src.cli --publish YYYY-MM-DD-slug
```

When prompted, paste the Notion page ID for that post. You can copy it from the Notion URL:
```
https://www.notion.so/...?v=xxx&pvs=4&p=<PAGE_ID>
```

This will:
- Set the status to "Published"
- Save the blog post URL to the "לינק לפוסט" field

## What Gets Saved to Notion

### After Generation
- ✅ `ניקוד` — Review score (0-10)
- ✅ `מילים` — Word count
- ✅ `Slug` — Post slug for reference
- ✅ Status → "Ready to Publish"

### After Publishing
- ✅ `לינק לפוסט` — Direct link to the published post
- ✅ Status → "Published"

### On Errors
- ✅ Status → "Error"

## Filtering & Tracking in Notion

You can now easily track your posts:

- **Filter by Status**: See which posts are In Progress, Ready to Publish, Published, etc.
- **Filter by Score**: Show only posts scoring 8+ if you want high-quality content
- **Sort by Word Count**: See your longest/shortest posts
- **Click "לינק לפוסט"** to go directly to the published blog post

## Tips

1. **Batch Generation**: Add 5-10 items to your Notion queue and run `--next` repeatedly
2. **Keep Notes**: Use Notion's comment feature to add notes about why something was generated or any issues
3. **Date Field**: You can use the "תאריך יצירה" (creation date) to track when items were added to your queue
4. **Reuse URLs**: If you want to regenerate a post, mark it as "Not started" again and run `--next` with `--no-dedup`

## Troubleshooting

**"Queue is empty" but I have items in Notion**
- Make sure the integration has access to your database (Settings → Connections)
- Check that items have "Not started" status AND a valid URL starting with http:// or https://

**"Error updating Notion"**
- Check that the field names match exactly (Hebrew spelling matters!)
- Verify the Notion token is still valid (it may expire)

**Missing Notion fields**
- The generator looks for specific field names. Check that your field names match exactly.
- If you renamed fields, either rename them back or update the code in `src/notion_client.py`

## Field Name Reference

If you need to customize field names, edit `src/notion_client.py`:

```python
# In fetch_next_article():
url_prop = props.get("URL מקור", {})  # Change this if needed
tags_prop = props.get("קטגוריה", {})  # Change this if needed

# In update_generation_metrics():
"ניקוד" — Score field name
"מילים" — Word count field name
"Slug" — Slug field name

# In update_blog_url():
"לינק לפוסט" — Blog post URL field name
```
