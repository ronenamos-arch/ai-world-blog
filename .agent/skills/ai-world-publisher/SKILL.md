---
name: ai-world-publisher
description: Workflow to fetch an article header and URL from Notion, translate/adapt it to Hebrew in the AI World blog voice, strip foreign ads/CTAs, categorize in Notion, create/embed header images, preview locally on Astro, and deploy on approval.
---

# AI World Blog - Notion-to-Publish Workflow

Use this skill when processing articles from the Notion content database into high-quality Hebrew blog posts on ai-world-blog.

## 1. Notion Integration & Queue Fetch

- Connect to Notion using the token in `env.txt` (or `.env`) and Database ID `33d927f0e15480ed8e8ad00e60e47fbb`.
- Fetch the specified row or the next item with `Status` = "Not started".
- Mark the Notion page `Status` as `In progress`.

## 2. Content Extraction & Filtering

- Fetch the source article from `URL מקור`.
- Extract key facts, tools, actionable takeaways, and step-by-step guides.
- **Strict Filtering**: Strip out all original website ads, sponsor banners, foreign affiliate links, and original CTAs.
- The post must be **independent**: never mention or link the source article, and do not add "מבוסס על..." attribution lines.

## 3. Hebrew Writing & Voice Guidelines

- **Tone**: Natural Israeli Hebrew in 2nd-person plural (אתם, תוכלו), direct and practical, zero machine-translation phrasing.
- **Terms**: Keep tool names, model names, and code/tech terms in English (e.g., Gemini, Claude, n8n, API, Python, Markdown).
- **Structure**:
  1. Frontmatter:
     `yaml
     ---
     title: "<Hebrew, benefit-led headline>"
     description: "<Hebrew, 1-2 practical sentences>"
     pubDatetime: <today>T<past-time-today>+03:00
     author: מומחה ה AI שלכם
     tags:
       - <3-5 relevant tags in Hebrew / Tool names>
     featured: false
     draft: false
     ogImage: /images/posts/<slug>.jpg
     ---
     `
  2. Opening: 2 paragraphs — the pain point, followed by the solution in bold.
  3. Numbered `##` sections with `### איך זה עובד?` or `### מה מקבלים?`, bullet lists (`•`), `### למה זה טוב?`, and `**למי מתאים:**`.
  4. Closing `## סיכום` with practical takeaways.
  - Note: About-the-Author box and Telegram CTA are injected automatically by `PostDetails.astro` layout.

## 4. Image Handling

- Check for quality content diagrams/screenshots from the source or user uploads.
- Save to `blog/public/images/posts/<slug>-*.png/jpg`.
- If a new cover image is needed, generate a clean 16:9 minimalist 3D graphic and save to `blog/public/images/posts/<slug>.jpg`.
- Reference in frontmatter as `ogImage: /images/posts/<slug>.jpg`.

## 5. Notion Metadata Sync

Update the page in Notion with:
- `Slug`: `<slug>`
- `Meta Description`: `<description>`
- `Alt Text`: `<image alt>`
- `קטגוריה`: Multi-select tags matching content (e.g. פרודוקטיביות, אוטומציה, Gemini)
- `מילים`: Word count
- `ניקוד`: Quality score (1-10)

## 6. Local Dev & Preview

- Save post file to `blog/src/data/blog/YYYY-MM-DD-<slug>.md`.
- Run `npx astro build` in `blog/` to ensure 0 build errors.
- Ensure dev server is running on `http://localhost:4321/`.
- Provide the user with the direct preview link: `http://localhost:4321/posts/YYYY-MM-DD-<slug>/`.
- **Stop and wait for human review.**

## 7. Deploy & Final Publish

When the user approves:
1. `git add` ONLY the markdown file, its images, and any requested site config files.
2. Commit: `Publish: <slug>`.
3. `git push origin main` (Vercel automatically deploys).
4. Update Notion properties:
   - `Status`: `Published`
   - `פורסם באתר`: `True`
   - `ביקורת אנושית`: `True`
   - `לינק לפוסט`: `https://ai-world-blog.vercel.app/posts/YYYY-MM-DD-<slug>/`
   - `תאריך פרסום`: Current date
5. Verify live post on `https://ai-world-blog.vercel.app/posts`.