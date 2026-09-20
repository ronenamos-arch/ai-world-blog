# עולם ה AI — בלוג אוטומטי בעברית

בלוג עברי אוטומטי על כלי AI, מדריכים נגישים, והסברים ישירים.

**Live:** https://ai-world-blog.vercel.app  
**Repo:** https://github.com/ronenamos-arch/ai-world-blog

---

## מבנה הפרויקט

```
Blog experimrement/
├── blog/          # אתר Astro (AstroPaper)
├── generator/     # Python pipeline לייצור פוסטים אוטומטי
├── docs/          # תיעוד
└── vercel.json    # הגדרות deploy
```

## הרצה מקומית

```bash
cd blog
pnpm install
pnpm run dev       # http://localhost:4321
pnpm run build     # בנייה לפרודקשן
```

## ייצור פוסט חדש

```bash
cd generator
.venv/Scripts/python -m src.cli --next              # פוסט הבא מהתור
.venv/Scripts/python -m src.cli --url <URL> --type tool_explainer  # URL ספציפי
.venv/Scripts/python -m src.cli --next --dry-run    # בדיקה בלי כתיבה
```

## GitHub Actions

הפעלה ידנית: GitHub → Actions → "Generate blog post" → Run workflow  
Cron אוטומטי: כל יום ראשון 10:00 שעון ישראל

---

## TODO — משימות לפגישה הבאה

### 1. תיקון Vercel Auto-Deploy (גבוה)
הגדרת Root Directory ב-Vercel Dashboard כדי ש-GitHub pushes יפרסמו אוטומטית בלי CLI.

- [ ] כנס ל-vercel.com → פרויקט `ai-world-blog` → Project Settings → General
- [ ] שנה **Root Directory** מ-`./` ל-`blog`
- [ ] לחץ Save — מהרגע הזה כל push ל-main יפרסם אוטומטית

---

### 2. תמונות לפוסטים (בינוני)
כרגע הפוסטים ריקים מתמונות. הוספת תמונה ראשית (OG image) ותמונות תוך-טקסטיות.

**אפשרויות לבדיקה:**
- **fal.ai Flux Schnell** — יצירת תמונה אוטומטית לפי נושא הפוסט (מהיר, ~0.5s)
- **Unsplash API** — חיפוש תמונה חופשית לפי מילות מפתח
- **Pexels API** — אלטרנטיבה ל-Unsplash

**מה צריך לבנות:**
- [ ] הוספת שלב `generate_image(title, tags)` ל-pipeline אחרי יצירת הפוסט
- [ ] שמירת תמונה ב-`blog/public/images/posts/`
- [ ] הוספת שדה `ogImage` ל-frontmatter אוטומטית
- [ ] תמונה ראשית (hero) בתוך הפוסט בשורה הראשונה אחרי ה-intro

---

### 3. Affiliate Backlinks (בינוני)
הכנסת קישורי שותפים רלוונטיים לכל פוסט בצורה מבוקרת.

**הארכיטקטורה המתוכננת:**
- [ ] יצירת קובץ `generator/affiliates.yaml` עם רשימת שותפים לפי קטגוריה:
  ```yaml
  affiliates:
    - name: Perplexity Pro
      url: https://...
      categories: [search, AI-tools]
      cta: "נסו Perplexity Pro בחינם"
    - name: Zapier
      url: https://...
      categories: [automation]
      cta: "התחילו עם Zapier בחינם"
  ```
- [ ] הוספת לוגיקה ל-pipeline: התאמת שותף לפי tags/post_type
- [ ] Claude מכניס את הקישור בצורה טבעית בסוף הפוסט (לא כבאנר)

---

### 4. CTA (קריאה לפעולה) — בלוג ופוסטים (נמוך)
הוספת CTA אחד ברור בכל פוסט ובדף הבית.

**מה צריך:**
- [ ] החלטה: מה ה-CTA? (הרשמה לרשימת תפוצה / RSS / ערוץ וואטסאפ / טלגרם)
- [ ] הוספת קומפוננט `CTA.astro` שמוצג בסוף כל פוסט
- [ ] הוספת CTA גם בדף הבית (מתחת לסעיף "פוסטים אחרונים")
- [ ] אינטגרציה של CTA ל-generator (Claude מוסיף בסוף כל פוסט)

---

## סטטוס נוכחי

| רכיב | סטטוס |
|---|---|
| בלוג Astro + RTL עברית | ✅ |
| Deploy ל-Vercel | ✅ (ידני בCLI) |
| Auto-deploy מ-GitHub | ⚠️ דורש הגדרה |
| Generator Python | ✅ |
| Firecrawl + Claude pipeline | ✅ |
| GitHub Actions (manual + cron) | ✅ |
| תמונות לפוסטים | ❌ |
| Affiliate links | ❌ |
| CTA קבוצת טלגרם | ❌ |
