---
name: ai-blog-autopilot
description: Full autonomous AI blog publisher and Notion pipeline runner for "עולם ה-AI" (AI World Blog). Automatically evaluates story candidates with Jev System-1 triage, generates Hebrew articles with Claude, assigns categories, injects monetization CTAs, ensures UI/code contrast and related post cards, updates Notion, deploys to production, and syncs Google Search Console.
---

# AI Blog Autopilot & Notion Publishing Pipeline

Activate this skill whenever the user asks to generate posts, review Notion rows, run Jev triage, fix pipeline issues, publish blog articles, deploy to production, or update Google Search Console for **עולם ה-AI** (`ai-world-blog`).

---

## 🏗️ Architecture & Core Components

```
┌─────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐
│  Notion Queue   │ ──> │ Jev System-1 Triage  │ ──> │ Claude 3.7 Generator │
│ (Status/Review) │     │ (Score, Tags, CTA)   │     │ (1,200+ Words Hebrew)│
└─────────────────┘     └──────────────────────┘     └──────────────────────┘
                                                                │
                                                                ▼
┌─────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐
│ GSC & Indexing  │ <── │ Git/Vercel Deploy    │ <── │ CTA & Related Cards  │
│ (Sitemap/Inspect│     │ (npm run publish)    │     │ (High-contrast UI)   │
└─────────────────┘     └──────────────────────┘     └──────────────────────┘
```

* **Target Production Site**: `https://ai-world-blog.vercel.app/`
* **Local Development Port**: `http://localhost:4321`
* **Primary Project Directory**: `00_website/` (Mirror in `blog/`)
* **GSC Management Client**: `02_scripts/01_seo_and_gsc/gsc_client.py`

---

## 📋 Notion Database Schema & Rules

When reading or updating Notion pages in the blog database, strictly use the verified schema fields:

| Field Name in Notion | Type | Usage / Notes |
| :--- | :--- | :--- |
| `Name` | `title` | Article title |
| `Status` | `status` | Options: `"ready to publish"`, `"In progress"`, `"published"`, `"Error"`, `"נדחה באיכות נמוכה"` |
| `פורסם באתר` | `checkbox` | `true` once deployed to live site |
| `פורסם בפייסבוק` | `checkbox` | `true` if shared to social channels |
| `ביקורת אנושית` | `checkbox` | Human approval flag. Pre-condition for publishing |
| `לינק לפוסט` | `url` | Full production URL (`https://ai-world-blog.vercel.app/posts/<slug>/`) |
| `תאריך פרסום` | `date` | ISO format `{ start: "YYYY-MM-DD" }` |
| `ניקוד` | `number` | Jev Quality Score (1-10) |
| `Meta Description` | `rich_text` | Concise 150-160 character SEO description |
| `הפוסט הסופי` | `rich_text` | Markdown post body. Chunk in max 2,000-char parts due to Notion API limit |
| `קטגוריה` | `multi_select` | List of tags: `[{ name: "..." }]` |
| `תמונה שנוצרה` | `files` | Post header or featured image |
| `URL מקור` | `url` | Source article / reference URL |
| `origin post ` | `rich_text` | Initial idea, raw prompt, or transcript |

> [!WARNING]
> Do NOT send non-existent properties like `Slug`, `Alt Text`, or `מילים` to the Notion API update call, as they will cause validation errors.

---

## ⚡ Jev System-1 Triage & Dynamic CTAs

1. **Jev Evaluation (`typesafe-ai/jev`)**:
   - Runs ultra-fast pre-flight screening (<150ms) via Vercel AI Gateway.
   - Evaluates: `qualityScore` (1-10), `suggestedPostType`, `targetAudience`, `commercialIntent`, `recommendedCta`, and `categories`.
   - Records an informative comment in Notion with score and reasoning.
   - Auto-populates `ניקוד` and `קטגוריה` properties.

2. **Monetization CTAs**:
   - `google_ai_pro_deal` (Priority Offer): Discount access link to Google AI Pro / Gemini Advanced (`https://google-ai-pro-drab.vercel.app/`).
   - `course`: AI Agents & Automation Masterclass.
   - `consulting`: Enterprise AI Implementation & Architecture.
   - `tools`: Recommended dev stacks and cloud AI infrastructure.
   - `newsletter`: VIP AI Insider updates.

---

## 🎨 Post Styling & UX Guidelines

Every generated post must comply with the following standards:

1. **Terminal & Code Block Styling**:
   - In raw HTML snippets or `<pre>` blocks, always enforce high contrast with dark background and white/bright text (`color: #ffffff; background: #0f172a;`).
2. **Related Post Cards (פוסטים נוספים ששווה לקרוא)**:
   - At the bottom of each article, include a grid/cards section pointing to 2-3 existing relevant articles on the blog.
   - Each card must include: thumbnail image path (`/images/posts/<name>.jpg`), publication date, title, description, and link.
3. **SEO & FAQ Schema**:
   - Include 3-5 structured FAQs in frontmatter for Google Rich Snippets and zero-click answer optimization.

---

## 🚀 Autonomous Execution Workflows

When the user asks in chat, execute the full workflow without asking them to run terminal commands:

### Workflow A: Generate Posts from Notion
1. Fetch candidates from Notion (`Status = "ready to publish"`).
2. Run Jev pre-flight triage and update Notion score/categories.
3. Generate 1,200+ word Hebrew article with Claude 3.7.
4. Inject selected Monetization CTA and related post cards.
5. Save Markdown in `00_website/00_src/data/blog/YYYY-MM-DD-<slug>.md` with `draft: true`.
6. Update Notion `הפוסט הסופי` and `Status = "In progress"`.

### Workflow B: Review & Local Preview
1. Start Astro preview server if not running:
   ```powershell
   npx astro preview --port 4321
   ```
2. Provide clickable link: `http://localhost:4321`.

### Workflow C: Production Deployment & GSC Indexing
1. Check approved posts (`ביקורת אנושית = true`) and set `draft: false`.
2. Run test build:
   ```powershell
   cd 'c:\Users\Ronen\Documents\Projects\repos\Blog experimrement\00_website'; npm run build
   ```
3. Commit and push to Git:
   ```powershell
   git add -A
   git commit -m "feat(content): publish new posts and update assets"
   git push origin main
   ```
4. **Submit to Google Search Console (GSC)**:
   - Refresh sitemap:
     ```powershell
     & 'C:\Python313\python.exe' 02_scripts/01_seo_and_gsc/gsc_client.py sitemap --site https://ai-world-blog.vercel.app/
     ```
   - Inspect and trigger indexing on every new URL:
     ```powershell
     & 'C:\Python313\python.exe' 02_scripts/01_seo_and_gsc/gsc_client.py inspect --url https://ai-world-blog.vercel.app/posts/<slug>/ --site https://ai-world-blog.vercel.app/
     ```
5. **Update Notion Table**:
   - Set `Status = "published"`, `פורסם באתר = true`, `לינק לפוסט = <live_url>`, `תאריך פרסום = "YYYY-MM-DD"`.

---

## 🔒 Redaction & Safety Rules
* **NEVER** output raw API keys, tokens, or service account secrets in chat messages.
* Always ensure `.env` and credential files remain in `.gitignore`.
