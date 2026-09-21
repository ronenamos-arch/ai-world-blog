---
name: ai-blog-autopilot
description: Full autonomous AI blog publisher and Notion pipeline runner for "עולם ה-AI" (AI World Blog). Automatically evaluates story candidates with Jev System-1 triage, generates Hebrew articles with Claude, assigns categories, injects monetization CTAs, and publishes to production without the user touching the terminal.
---

# AI Blog Autopilot & Jev Triage Assistant

Activate this skill whenever the user asks in chat to generate posts, check Notion, test ideas, run Jev triage, review drafts, or publish blog articles for **עולם ה-AI** (`Blog experimrement`).

---

## 🎯 Conversational Commands & Actions

The user does NOT need to use the terminal. Execute all actions autonomously using `run_command` in the background and report structured results in Hebrew:

### 1. "תבדוק את נושן" / "תריץ סינון של Jev" / "תבדוק רעיונות"
* **Action**: Run the Jev pre-flight evaluation and test suite or check pending Notion items.
* **Execution**:
  ```powershell
  cd 'c:\Users\Ronen\Documents\Projects\repos\Blog experimrement\00_website'; npm run test:jev
  ```
* **Output**: Report which ideas passed/failed, scores, recommended categories, and CTA goals.

### 2. "תייצר פוסטים" / "תריץ את ה-Pipeline" / "Generate posts"
* **Action**: Execute the end-to-end generation workflow:
  1. Fetch items with `Status = "ready to publish"` from Notion.
  2. Run Jev System-1 triage (score, category auto-tagging, audience mapping).
  3. Generate full 1,200+ word Hebrew article with Claude.
  4. Inject dynamic monetization CTA (`course`, `consulting`, `tools`, `newsletter`).
  5. Save to Notion (`הפוסט הסופי`, comments, categories) and create Markdown file in `00_website/00_src/data/blog/`.
* **Execution**:
  ```powershell
  cd 'c:\Users\Ronen\Documents\Projects\repos\Blog experimrement\00_website'; npm run generate
  ```
* **Output**: Summary of generated posts, word counts, Jev scores, and next steps.

### 3. "תפרסם לאתר" / "תעלה ל-Production" / "Publish"
* **Action**: Check for approved posts (where `ביקורת אנושית` checkbox is ticked in Notion), update drafts to `draft: false`, build the Astro site, and push to production.
* **Execution**:
  ```powershell
  cd 'c:\Users\Ronen\Documents\Projects\repos\Blog experimrement\00_website'; npm run publish
  ```
* **Output**: Report published URLs and build status.

### 4. "תציג לי תצוגה מקדימה" / "Start preview"
* **Action**: Launch the local Astro development server on port 4321 and provide clickable link: `http://localhost:4321`.

---

## 🛡️ Security & Integrity Guidelines
* **Secrets**: Never display API keys, tokens, or credentials in chat outputs. Always mask or redact them.
* **Notion Sync**: Ensure Notion comments and categories are updated accurately with Jev feedback.
