# Setting Up Notion Statuses for Phase 2

Your Notion database currently only has "Done" and "Not started" statuses. To fully use Phase 2 features, add these new statuses:

## How to Add Statuses in Notion

1. Open your "חומר לאתר AI-WORLD-BLOG" database in Notion
2. Click on the **Status** column header
3. Select **Edit property** (or click the dropdown arrow)
4. Under "Options", click **Add another option** and add these statuses:

### Required Statuses to Add

| Status | Color | Purpose |
|--------|-------|---------|
| In Progress | Yellow/Orange | Currently being generated |
| Ready to Publish | Blue | Generated, awaiting manual review |
| Published | Green | Live on the blog |
| Error | Red | Generation failed |

**Keep the existing ones:**
- ✅ Not started
- ✅ Done (can be retired, but keep it for now)

## Visual Flow

```
Not started
    ↓
In Progress (automatic)
    ↓
Ready to Publish (automatic after generation)
    ↓ (manual: change draft to false and push)
    ↓
Published (automatic after running --publish)
```

---

## If You Don't Want to Add Statuses Yet

The code will work with just **"Done"** and **"Not started"** but you'll lose some tracking:

- ✅ Posts still generate
- ✅ Metrics still save (score, word count, slug)
- ❌ No "In Progress" tracking
- ❌ Error status falls back to "Done"
- ❌ No "Ready to Publish" distinction

**Recommendation:** Add the 4 statuses above (takes 2 minutes). It greatly improves your workflow visibility.

---

## After Adding Statuses

1. Verify they appear in the Status column dropdown
2. Run `python -m src.cli --next` again
3. Watch the status change: Not started → In Progress → Ready to Publish

Done! 🎉
