---
description: Create a Hebrew blog post from a URL, preview on localhost, deploy on approval
argument-hint: <source-url>
---

# Create Post from URL

The user gives you a source URL: $ARGUMENTS

Follow this workflow end-to-end. Do not skip the preview/approval step.

## 1. Research

- Fetch the source URL (WebFetch) and extract: the core news/argument, all key facts, pricing, tool names, and practical takeaways.
- Read the most recent post in `blog/src/data/blog/` (by `pubDatetime`) to match its tone and structure.

## 2. Images

- Check `blog/public/images/posts/` for images the user already saved for this post (recently added files). If images relevant to the topic exist, use them.
- If none exist, try to download the article's main images into `blog/public/images/posts/<slug>-*.{jpg,png}` (only content images, not ads/logos). If nothing usable can be downloaded, ask the user to drop images into that folder and tell them the filenames you expect.
- Pick one image as `ogImage`; embed the rest inline at relevant sections.
- The layout renders `ogImage` below the headline automatically — do NOT also embed the ogImage inline in the body.

## 3. Write the post

Create `blog/src/data/blog/YYYY-MM-DD-<slug>.md` (today's date, English kebab-case slug). The `<slug>` part must be max 2 words (1-2 words, short and punchy — e.g. `claude-improve`, not `continually-improve-claude-code`).

Frontmatter (exactly this shape — `ogImage` is a plain public path string, never an import):

```yaml
---
title: "<Hebrew, benefit-led>"
description: "<Hebrew, 1-2 sentences>"
pubDatetime: <today>T<current time, MUST be in the past — posts with a future pubDatetime are hidden from the production listing>+03:00
author: מומחה ה AI שלכם
tags: [3-5 relevant tags, Hebrew or tool names]
featured: false
draft: false
ogImage: /images/posts/<file>
---
```

Body structure (mirror existing posts):
- Opening: 2 paragraphs — the pain point, then the solution in bold.
- Numbered `##` sections, each with: short intro, "### איך זה עובד?" or "### מה מקבלים?" bullet list (• bullets), optionally "### למה זה טוב?", a "**למי מתאים:**" line, and an external CTA link where relevant.
- Closing `## סיכום` section.
- **Independent post**: never mention or link the source article. No "מבוסס על..." attribution line.
- The About-the-Author box and Telegram CTA are added automatically by the layout — do not add them.

### Hebrew quality rules (mandatory)

- Natural, readable Israeli Hebrew — second-person plural (אתם), direct and practical, no machine-translation phrasing.
- Keep product/tool names, model names, and code terms in English (Claude, IDE, API, Markdown).
- Proofread the final text: no mixed-script typos (Latin letters inside Hebrew words), no broken nikud/gibberish, correct gender agreement, numbers/prices formatted like $20.
- Read the whole post once after writing and fix anything that doesn't read naturally.

## 4. Preview

- Start the dev server if not already running: `npx astro dev` in `blog/` (background). Note: `pnpm` is not on PATH — use `npx`. Check first with a request to `http://localhost:4321/` — don't start a second server.
- Note: `draft: true` posts are hidden even in dev — that's why the frontmatter uses `draft: false`; safety comes from not pushing until approval.
- Run `npx astro build` in `blog/` to confirm the build passes.
- Give the user the localhost URL: `http://localhost:4321/posts/<filename-without-.md>/`
- **Stop and wait for the user's review.** Do not commit or push yet.

## 5. Deploy (only after user approval)

When the user approves (says "publish", "deploy", "approve", "no changes", etc.):

- `git add` ONLY: the post file and its images. Never add unrelated untracked files.
- Commit: `Publish: <slug>` and push to `main`. Vercel deploys automatically.
- Report the live URL: `https://ai-world-blog.vercel.app/posts/<slug>/`
- After deploy, verify the post appears on `https://ai-world-blog.vercel.app/posts` (the listing). If missing, the usual cause is a future `pubDatetime` — fix and re-push.

## Hard rules

- Never create or edit `vercel.json`.
- Never change the build script in `blog/package.json`.
- Images always go in `blog/public/images/posts/` and are referenced as `/images/posts/...` strings.
- If the user requests changes during preview, apply them and let them re-review before deploying.
