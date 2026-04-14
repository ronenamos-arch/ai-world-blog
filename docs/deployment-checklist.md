# Blog Post Deployment Checklist

This document prevents the common issue of posts not appearing after deployment. **Read this before publishing any post.**

---

## ⚠️ The Critical Issue

**Posts with `draft: true` will NOT appear on the live blog**, even after Vercel deploys successfully.

This has happened twice:
1. Generator creates posts with `draft: true` by default
2. Posts are committed and pushed
3. Vercel deploys successfully ✓
4. But posts don't appear on the site ✗

**Root cause:** The frontmatter `draft: true` setting hides draft posts from the published blog.

---

## ✅ Pre-Deployment Checklist

Before you commit and push a new blog post, verify:

### 1. Check the Frontmatter

Open the post file and confirm:

```yaml
---
title: "Post Title"
description: "Short description"
pubDatetime: 2026-04-14T12:00:00+03:00
author: עולם ה AI
tags:
  - Tag1
  - Tag2
featured: false
draft: false          # ← THIS MUST BE 'false' TO PUBLISH
ogImage: /images/posts/your-image.jpg
---
```

**The key line:** `draft: false`

### 2. Verify the Image

```bash
# Check image exists
ls -lh blog/public/images/posts/your-image.jpg

# Confirm the path in frontmatter matches
ogImage: /images/posts/your-image.jpg  # Must start with /images/posts/
```

### 3. Test Locally (If Available)

```bash
cd blog
npm run dev
# Visit http://localhost:3000 and check if your post appears
```

### 4. Commit Message Format

```bash
git commit -m "publish: [Post Title] - brief description"
# Example: "publish: GitHub for Beginners - Hebrew tutorial"
```

### 5. After Push

**Wait for Vercel deployment to complete:**
1. Push code: `git push`
2. Check Vercel: https://vercel.com/ronenamos-archs-projects/ai-world-blog
3. Wait for "Deployment successful" ✓
4. Visit blog: https://ai-world-blog.vercel.app
5. Search for your post title (use browser find or scroll)

---

## 📋 Quick Checklist Template

Copy this for each post:

```
[ ] Opened post file
[ ] Confirmed draft: false (NOT draft: true)
[ ] Image file exists: blog/public/images/posts/
[ ] Image path in frontmatter: /images/posts/your-image.jpg
[ ] Committed with clear message
[ ] Pushed to GitHub
[ ] Verified Vercel deployment status
[ ] Post appears on live blog
[ ] Post URL works: https://ai-world-blog.vercel.app/YYYY-MM-DD-slug/
```

---

## 🔧 How to Fix if Post Doesn't Appear

If you've already pushed and Vercel deployed but post still doesn't show:

1. **Check the setting:**
   ```bash
   grep "draft:" blog/src/data/blog/YYYY-MM-DD-your-post.md
   ```
   If it says `draft: true`, continue to step 2.

2. **Change to published:**
   ```bash
   # Edit the file and change draft: true → draft: false
   ```

3. **Commit and push:**
   ```bash
   git add blog/src/data/blog/YYYY-MM-DD-your-post.md
   git commit -m "fix: publish post"
   git push
   ```

4. **Wait for Vercel** to redeploy and verify on the live site.

---

## 🚀 Generator Pipeline

When using the generator (`python -m src.cli --next`):

1. Generator creates posts with `draft: true` **automatically**
2. This is by design - manual review before publishing
3. **You must change `draft: false` before the post appears**
4. Follow the checklist above after changing it

---

## 📝 Post File Location

All blog posts go here:
```
blog/src/data/blog/YYYY-MM-DD-slug-name.md
```

Example:
```
blog/src/data/blog/2026-04-14-github-for-beginners.md
```

---

## 🎯 Summary

| Step | Check | Status |
|------|-------|--------|
| Edit post | `draft: false` | ✓ |
| Add image | File exists | ✓ |
| Commit | Clear message | ✓ |
| Push | `git push` | ✓ |
| Deploy | Vercel successful | ✓ |
| Verify | Post visible online | ✓ |

**If any step is missing, the post won't appear.**

---

## Questions?

- **Post still not showing?** → Check `draft: false` first
- **Image not loading?** → Verify path: `/images/posts/filename.jpg`
- **Can't find post on blog?** → Use Ctrl+F to search page
