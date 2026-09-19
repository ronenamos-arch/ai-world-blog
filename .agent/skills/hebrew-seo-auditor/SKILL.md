---
name: hebrew-seo-auditor
description: Comprehensive On-Page, Semantic, and Technical SEO auditor for Hebrew blog posts and pages on ai-world-blog. Audits search intent matching, Hebrew keyword entities, meta length, heading structure, image alt text, internal linking opportunities, and schema validation.
---

# Hebrew SEO Auditor for AI World Blog

Use this skill to perform a deep On-Page and Technical SEO audit on any Hebrew article, tag page, or site section, providing an actionable 1–100 SEO score, identified gaps, and ready-to-paste optimizations.

## How to Trigger
- Natural language:
  - "בצע ביקורת SEO על הפוסט <שם/קובץ>"
  - "תבדוק SEO על הפוסט האחרון"
  - "Run SEO audit on <post-slug/file>"
  - Or mention @hebrew-seo-auditor.

---

## Audit Checklist & Evaluation Criteria

When auditing an article (e.g. in `blog/src/data/blog/*.md`), systematically evaluate the following 6 pillars:

### 1. Title & Meta Description Optimization (25 Points)
- **Title Tag (`title` in frontmatter)**:
  - Length: Ideal between 45–60 characters (including ` | עולם ה AI`).
  - Keyword placement: Target Hebrew search query / tool name front-loaded in the first 30 characters.
  - Hook/Benefit: Includes a clear promise/value (e.g., "מדריך מעשי", "ב-5 צעדים", "בלי לכתוב קוד").
- **Meta Description (`description` in frontmatter)**:
  - Length: 120–160 characters in natural Hebrew.
  - Call to value: Explains precisely what the reader will learn or achieve.
  - Keyword inclusion: Contains primary keyword and 1 secondary entity.

### 2. Search Intent & Semantic Content Quality (25 Points)
- **Search Intent Match**: Does the article solve a real, high-intent query (Tutorial / Comparison / Problem-Solution)?
- **Hebrew Phrasing**: 100% natural Israeli Hebrew (אתם, תוכלו) with 0 machine-translation awkwardness.
- **Entity Density (NLP/BERT)**: Maintains appropriate technical English names (Gemini, Claude, n8n, Python, API) surrounded by clear Hebrew context.
- **EEAT (Experience & Authority)**: Clear, practical takeaways, code/step examples, and actionable setup guides.

### 3. Heading Architecture & Readability (15 Points)
- **H1**: Single H1 (the title), matching the core search topic.
- **H2 & H3 Semantic Hierarchy**:
  - Logical flow: Introduction / Pain point -> How it works -> Step-by-step guide -> Summary (`## סיכום`).
  - Descriptive headings containing relevant search variants (e.g., `## איך להגדיר את הכלי?`, `### שלב 1: חיבור ה-API`).
- **Formatting**: Short paragraphs (2–4 lines max), bullet points (`•`), and bold emphasis on key terms.

### 4. Visual SEO & Image Optimization (15 Points)
- **Cover Image (`ogImage`)**: Exists in `blog/public/images/posts/` and is 16:9 high resolution.
- **Image Alt Tags**:
  - **MANDATORY**: Every markdown image `![alt](path)` MUST have descriptive Hebrew alt text (e.g., `![צילום מסך של הגדרות ה-API ב-Google AI Studio](/images/posts/...)`).
  - Reject empty alt tags (`![]`) or generic English filenames as alt.
- **Visual Diversity**: Checks for inline infographics, workflow diagrams, or UI screenshots.

### 5. Internal Linking & Topic Clusters (10 Points)
- **Outbound Internal Links**: The post should link to 2–4 existing relevant posts in `blog/src/data/blog/` using contextual Hebrew anchor text (e.g., `במדריך שלנו על [סוכני Claude](url) תוכלו לראות...`).
- **Inbound Linking Opportunities**: Identify which other existing posts should link *to* this new article.

### 6. Rich Snippets & FAQ Opportunities (10 Points)
- **FAQ Section**: Suggest 2–3 high-intent question-and-answer pairs matching Google's "People Also Ask" (שאילתות קשורות) for the topic.

---

## Output Report Format

Always present the audit in this structured Hebrew markdown format:

````markdown
# 🔍 דוח ביקורת SEO: [שם הפוסט]

**ציון SEO כולל:** [X/100] ⭐

---

### 📊 סיכום לפי קטגוריות
| קטגוריה | ציון | סטטוס |
| :--- | :--- | :--- |
| כותרת ותיאור מטא | X/25 | ✅ / ⚠️ / ❌ |
| כוונת חיפוש ואיכות תוכן | X/25 | ✅ / ⚠️ / ❌ |
| מבנה כותרות וקריאות | X/15 | ✅ / ⚠️ / ❌ |
| תמונות ו-Alt Tags | X/15 | ✅ / ⚠️ / ❌ |
| קישורים פנימיים (Internal Links) | X/10 | ✅ / ⚠️ / ❌ |
| סכמה ו-FAQ Rich Snippets | X/10 | ✅ / ⚠️ / ❌ |

---

### ✅ נקודות חוזק (Passed Checks)
- [רשימת הדברים שמבוצעים מעולה]

---

### ⚠️ שיפורים מומלצים (Action Items)

#### 1. שיפור כותרת ותיאור מטא (אם נדרש)
- **כותרת נוכחית:** `...` (X תווים)
- **כותרת מומלצת:** `...` (Y תווים)
- **תיאור נוכחי:** `...` (X תווים)
- **תיאור מומלץ:** `...` (Y תווים)

#### 2. תגיות Alt לתמונות
- [הצעת תגיות Alt בעברית לכל התמונות בפוסט]

#### 3. הצעות לקישורים פנימיים (Internal Linking)
- **קשר לפוסטים קיימים:**
  - לקשר אל: `[שם פוסט קיים](נתיב)` עם אנקור: *"טקסט עוגן בעברית"*
  - לקשר אל: `[שם פוסט נוסף](נתיב)` עם אנקור: *"טקסט עוגן נוסף"*

#### 4. שאלות נפוצות מומלצות לתוספת (FAQ Snippets)
```markdown
## שאלות נפוצות

### [שאלה ממוקדת חיפוש 1]
[תשובה קצרה וישירה של 2-3 משפטים]

### [שאלה ממוקדת חיפוש 2]
[תשובה קצרה וישירה של 2-3 משפטים]
```
````

---

## Automatic Fix Mode

When the user asks to "apply the fixes" / "תקן את הפוסט לפי הביקורת":
1. Update the frontmatter (`title`, `description`, `tags`).
2. Add Hebrew `alt` text to images.
3. Inject the contextual internal links into the markdown body.
4. Append the FAQ section if approved.
5. Re-run `npx astro build` in `blog/` to ensure zero syntax or build errors.
