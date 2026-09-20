# 🗂️ אינדקס ומפת הפרויקט: AI World Blog

ברוכים הבאים למאגר המרכזי של **עולם ה-AI (AI World Blog)**.  
מסמך זה מרכז את המבנה המלא של התיקייה, תפקידו של כל קובץ, וקישורים ישירים לכל החלקים בפרויקט.

---

## 🧭 מפת מבנה התיקייה הראשית (High-Level Architecture)

```
📂 Blog experimrement/ (Root)
│
├── 🌐 blog/                   ← פרויקט האתר (Astro + Tailwind + TypeScript)
├── ⚙️ generator/              ← מנוע אוטומטי ליצירת פוסטים מ-Notion/AI
├── 🐍 scripts/                ← סקריפטים עצמאיים (GSC, Notion, FB Sync)
├── 📚 docs/                   ← מסמכי תיעוד, נהלים ואסטרטגיה
├── 🤖 .agent/ & .claude/      ← מיומנויות סוכן וקונפיגורציית AI
├── 👤 Ronen/                  ← הערות אישיות ותוכניות עבודה של רונן
├── 📝 logs/                   ← קובצי לוגים ופלט ריצות
└── 🔑 קובצי שורש              ← הגדרות, מפתחות ואינדקס מרכזי
```

---

## 📑 פירוט מלא של כל הקבצים והתיקיות בפרויקט

### 1. 🌐 פרויקט הבלוג (`/blog`) - אתר האינטרנט
אתר הבלוג בנוי ב-Astro (תבנית מבוססת AstroPaper מותאמת אישית לעברית ול-RTL).

| קובץ / תיקייה | תיאור ותפקיד |
| :--- | :--- |
| [`blog/astro.config.ts`](file:///c:/Users/Ronen/Documents/Projects/repos/Blog%20experimrement/blog/astro.config.ts) | הגדרות Astro, אינטגרציית Sitemap, פונטים בעברית (Heebo) ו-Tailwind |
| [`blog/src/config.ts`](file:///c:/Users/Ronen/Documents/Projects/repos/Blog%20experimrement/blog/src/config.ts) | הגדרות מטא כלליות של האתר (`title`, `author`, `timezone`, `website`) |
| [`blog/src/data/blog/`](file:///c:/Users/Ronen/Documents/Projects/repos/Blog%20experimrement/blog/src/data/blog) | **כל מאמרי הבלוג (40+ פוסטי Markdown בעברית)** |
| [`blog/src/layouts/`](file:///c:/Users/Ronen/Documents/Projects/repos/Blog%20experimrement/blog/src/layouts) | תבניות העמודים (`PostDetails.astro`, `Layout.astro`, `BaseHead.astro`) |
| [`blog/src/components/`](file:///c:/Users/Ronen/Documents/Projects/repos/Blog%20experimrement/blog/src/components) | רכיבי UI (`LeadGen.astro`, `LeadPopup.astro`, `Header.astro`, `Card.astro`) |
| [`blog/public/images/posts/`](file:///c:/Users/Ronen/Documents/Projects/repos/Blog%20experimrement/blog/public/images/posts) | תמונות ראשראשיות (OG Images) ותרשימים למאמרים |

---

### 2. ⚙️ מנוע יצירת הפוסטים (`/generator`) - אוטומציית תוכן
מערכת Python מודולרית למשיכת רעיונות מ-Notion, יצירת טיוטות באמצעות Claude/Gemini, והמרתן לפוסטי Markdown.

| קובץ / תיקייה | תיאור ותפקיד |
| :--- | :--- |
| [`generator/src/cli.py`](file:///c:/Users/Ronen/Documents/Projects/repos/Blog%20experimrement/generator/src/cli.py) | ממשק שורת פקודה להרצת תהליך יצירת הפוסטים |
| [`generator/src/pipeline.py`](file:///c:/Users/Ronen/Documents/Projects/repos/Blog%20experimrement/generator/src/pipeline.py) | ניהול צינור העבודה המלא מקריאת Notion ועד שמירת הקובץ |
| [`generator/src/claude_client.py`](file:///c:/Users/Ronen/Documents/Projects/repos/Blog%20experimrement/generator/src/claude_client.py) | חיבור ל-API של Anthropic ליצירת תוכן בעברית |
| [`generator/src/notion_client.py`](file:///c:/Users/Ronen/Documents/Projects/repos/Blog%20experimrement/generator/src/notion_client.py) | משיכת משימות ורעיונות מדאטאבייס ה-Notion |
| [`generator/src/markdown_writer.py`](file:///c:/Users/Ronen/Documents/Projects/repos/Blog%20experimrement/generator/src/markdown_writer.py) | יצירת קובץ ה-Markdown עם Frontmatter מותאם לבלוג |
| [`generator/prompts/`](file:///c:/Users/Ronen/Documents/Projects/repos/Blog%20experimrement/generator/prompts) | פרומפטים מובנים לפי סוגי פוסטים (`tutorial.md`, `comparison.md`, `tool_roundup.md`) |
| [`generator/state/`](file:///c:/Users/Ronen/Documents/Projects/repos/Blog%20experimrement/generator/state) | קבצי שמירת מצב (`processed.json`, `queue.yaml`) למניעת כפילויות |

---

### 3. 🐍 סקריפטים עצמאיים וכלי עזר (`/scripts`)
כלי ניטור, סנכרון ו-SEO עצמאיים.

| קובץ / תיקייה | תיאור ותפקיד |
| :--- | :--- |
| [`scripts/gsc_client.py`](file:///c:/Users/Ronen/Documents/Projects/repos/Blog%20experimrement/scripts/gsc_client.py) | שליפת נתוני Search Console (קליקים, חשיפות, שאילתות, אינדוקס) |
| [`scripts/sync_notion_2_posts.py`](file:///c:/Users/Ronen/Documents/Projects/repos/Blog%20experimrement/scripts/sync_notion_2_posts.py) | סנכרון מאמרים ומטא-דאטה ישירות מ-Notion |
| [`scripts/validate_fb_posts.py`](file:///c:/Users/Ronen/Documents/Projects/repos/Blog%20experimrement/scripts/validate_fb_posts.py) | ולידציה ובדיקה של פוסטים ייעודיים לפייסבוק |
| [`scripts/notion-debug/`](file:///c:/Users/Ronen/Documents/Projects/repos/Blog%20experimrement/scripts/notion-debug) | כלי בדיקה ודיבוג לקריאות API של Notion |

---

### 4. 📚 תיעוד, אסטרטגיה ונהלים (`/docs`)

| קובץ / תיקייה | תיאור ותפקיד |
| :--- | :--- |
| [`docs/plans/SEO_GROWTH_TRACKER.md`](file:///c:/Users/Ronen/Documents/Projects/repos/Blog%20experimrement/docs/plans/SEO_GROWTH_TRACKER.md) | **📍 יומן הביצוע המרכזי של תוכנית הצמיחה (90 יום)** |
| [`docs/deployment-checklist.md`](file:///c:/Users/Ronen/Documents/Projects/repos/Blog%20experimrement/docs/deployment-checklist.md) | צ'קליסט מלא לבדיקה לפני פריסה ב-Vercel |
| [`docs/notion-integration-guide.md`](file:///c:/Users/Ronen/Documents/Projects/repos/Blog%20experimrement/docs/notion-integration-guide.md) | מדריך אינטגרציה מפורט ל-Notion |
| [`docs/voice-guide.md`](file:///c:/Users/Ronen/Documents/Projects/repos/Blog%20experimrement/docs/voice-guide.md) | הנחיות טון וסגנון כתיבה בעברית לבלוג עולם ה-AI |
| [`docs/research-reference.md`](file:///c:/Users/Ronen/Documents/Projects/repos/Blog%20experimrement/docs/research-reference.md) | מקורות מידע ומאגרי מחקר לתוכן |

---

### 5. 🤖 מיומנויות AI וסוכנים (`/.agent` & `/.claude`)

| קובץ / תיקייה | תיאור ותפקיד |
| :--- | :--- |
| [`.agent/skills/hebrew-seo-auditor/SKILL.md`](file:///c:/Users/Ronen/Documents/Projects/repos/Blog%20experimrement/.agent/skills/hebrew-seo-auditor/SKILL.md) | מיומנות בדיקת SEO On-Page מלאה בעברית (כולל ציון 1–100) |
| [`.agent/skills/ai-world-publisher/SKILL.md`](file:///c:/Users/Ronen/Documents/Projects/repos/Blog%20experimrement/.agent/skills/ai-world-publisher/SKILL.md) | מיומנות פרסום פוסטים מ-Notion עד ל-Astro |
| [`CLAUDE.md`](file:///c:/Users/Ronen/Documents/Projects/repos/Blog%20experimrement/CLAUDE.md) | הוראות מערכת והנחיות עבודה לסוכני Claude |
| [`assistant.md`](file:///c:/Users/Ronen/Documents/Projects/repos/Blog%20experimrement/assistant.md) | הגדרות עוזר ופרוטוקול עבודה |

---

### 6. 👤 הערות אישיות ותוכניות (`/Ronen`)

| קובץ / תיקייה | תיאור ותפקיד |
| :--- | :--- |
| [`Ronen/PLan to work on.txt`](file:///c:/Users/Ronen/Documents/Projects/repos/Blog%20experimrement/Ronen/PLan%20to%20work%20on.txt) | רעיונות ראשוניים, מודלים עסקיים, ערוצי רווח ודגשים של רונן |

---

### 7. 🔑 קבצי קונפיגורציה, מפתחות ולוגים (Root)

| קובץ | תיאור ותפקיד |
| :--- | :--- |
| `gsc-credentials.json` | מפתח Service Account מאובטח לחיבור ל-Google Search Console API |
| [`CHANGELOG.md`](file:///c:/Users/Ronen/Documents/Projects/repos/Blog%20experimrement/CHANGELOG.md) | יומן תיעוד שינויים היסטורי בפרויקט |
| `README.md` | הסבר כללי על המאגר |
| `output.txt` / `urls_output.txt` | קבצי פלט וריצות קודמות (שמורים לצורכי היסטוריה) |
| `rollback.py` | סקריפט בטיחות לשחזור פעולות ארגון תיקיות |

---

## 🚀 פקודות שימושיות מהירות (Quickstart)

```bash
# הרצת הבלוג מקומית לצפייה מוקדמת:
cd blog
npm run dev

# בניית הבלוג ובדיקת תקינות מלאה:
cd blog
npm run build

# הרצת בדיקת סרצ' קונסול:
python scripts/gsc_client.py
```
