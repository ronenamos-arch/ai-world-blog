# CLAUDE.md — AI Agent Instructions for This Project

This file tells AI agents (Claude, Gemini, etc.) how this project works and what mistakes to avoid. **Read this file before making any changes.**

---

## Project Overview

This is a monorepo:
```
Blog experimrement/
├── blog/          ← Astro blog (deployed to Vercel)
├── generator/     ← Python pipeline that generates posts
└── docs/          ← Documentation
```

---

## ⚠️ Critical Rules — Read Before Any Changes

### 1. Never create or edit `vercel.json`

The Vercel dashboard is configured with:
- **Root Directory: `blog`**
- **Framework: Astro**
- No custom commands needed

A `vercel.json` at the repo root **overrides** these dashboard settings and breaks deployment. This caused multiple failed builds in April 2026.

**If you are asked to "fix Vercel deployment", do NOT create a `vercel.json`. Instead:**
1. Check the dashboard settings first (Root Dir, Framework Preset)
2. Check the actual build logs for the specific error
3. Fix the root cause in code, not in Vercel config

See: [`docs/deployment-lessons.md`](docs/deployment-lessons.md)

---

### 2. Blog post images: always use `public/` with `z.string()` schema

Images for blog posts are stored in `blog/public/images/posts/`. They are **static files**, not Astro-processed assets.

- **Schema type:** `ogImage: z.string().optional()` ← use only this
- **Frontmatter format:** `ogImage: /images/posts/my-post.jpg` ← absolute public path
- **Do NOT use** `image()` from Astro's content schema for these images — it tries to import files at build time and will fail with `[ImageNotFound]`

See: [`docs/deployment-lessons.md`](docs/deployment-lessons.md)

---

### 3. Build script: keep it simple

Current `blog/package.json` build script:
```json
"build": "astro build"
```

Do NOT add `astro check`, `pagefind`, or `cp` commands to the build script — these have caused failures on Vercel in the past. Use `build:full` locally if you need pagefind.

---

### 4. Check deployment-lessons.md before debugging Vercel failures

Before spending time guessing at Vercel errors:
1. Read [`docs/deployment-lessons.md`](docs/deployment-lessons.md)
2. Look at the **actual Vercel build logs** (not just the error badge)
3. The logs are at: `https://vercel.com/ronenamos-archs-projects/ai-world-blog` → click the latest deployment → Build Logs

---

## Vercel Architecture

```
GitHub push to main
       ↓
Vercel detects change in blog/ (Root Directory)
       ↓
pnpm install  (auto-detected from pnpm-lock.yaml)
       ↓
astro build   (output → blog/dist/)
       ↓
Serves blog/dist/ as static site
```

**Live URL:** https://ai-world-blog.vercel.app  
**Repo:** https://github.com/ronenamos-arch/ai-world-blog

---

## Adding a New Blog Post

1. Create `blog/src/data/blog/YYYY-MM-DD-slug.md` with frontmatter:
   ```yaml
   ---
   title: "Post Title"
   description: "Short description"
   pubDatetime: 2026-04-09T10:00:00+03:00
   author: עולם ה AI
   tags:
     - AI
   featured: false
   draft: false
   ogImage: /images/posts/slug.jpg
   ---
   ```
2. Save the post image to `blog/public/images/posts/slug.jpg`
3. Push — Vercel auto-deploys

**Note:** Every post automatically includes an "About the Author" section (רונן עמוס - יועץ CFO חיצוני ומומחה AI לפיננסים) before the Telegram CTA. This is part of `blog/src/layouts/PostDetails.astro` and applies to all posts — no per-post configuration needed.

---

## Generator Pipeline (`generator/`)

```bash
cd generator
.venv/Scripts/python -m src.cli --next              # next from queue
.venv/Scripts/python -m src.cli --url <URL>          # specific URL
.venv/Scripts/python -m src.cli --next --dry-run     # test without writing
```

All generated posts start as `draft: true`. Manual approval required before changing to `draft: false`.
