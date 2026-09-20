# בלוג אוטומטי עם AstroPaper ו-Claude

## סקירה כללית

המטרה היא להקים בלוג סטטי מבוסס Astro (תבנית AstroPaper) ולהוסיף אליו צינור אוטומטי שמייצר פוסטים חדשים בעזרת Claude דרך ה-API, עם ריצה ידנית או אוטומטית (GitHub Actions / cron).[^1][^2][^3]

הארכיטקטורה תתבסס על ריפו בלוג (AstroPaper), ריפו/סקריפט גנרטור תוכן (Blog-Generator-Claude או קוד דומה), ואוטומציה שמייצרת קבצי Markdown, מכניסה אותם לתיקיית הבלוג, מבצעת commit ו-deploy אוטומטי (למשל ל-Vercel או GitHub Pages).[^4][^3][^1]

## רכיב 1: תבנית הבלוג – AstroPaper

AstroPaper היא תבנית בלוג מינימליסטית, רספונסיבית, נגישה וידידותית ל-SEO הבנויה עם Astro, Tailwind ו-TypeScript, ומתאימה לבלוגים טכנולוגיים ארוכי טווח.[^3]

הריפו הרשמי satnaing/astro-paper מספק תבנית מוכנה לגמרי עם פוסטים לדוגמה, RSS, תגיות ותשתית SEO, כך שאפשר להתחיל מ-fork או משימוש בה כ-template בפרויקט חדש.[^2][^3]

### יתרונות AstroPaper לפרויקט שלך

- מינימליות וניקיון – מתאים לתוכן מקצועי על AI וחדשנות בלי עומס עיצובי.[^3]
- SEO ו-RSS מובנים – חשוב לבלוג אוטומטי שמייצר הרבה תכנים שצריכים להיסרק בגוגל ולהישלח כ-feed.[^2][^3]
- קוד פתוח עם קהילה פעילה ו-Issues מסודרים, כך שקל להבין מבנה ולהרחיב.[^3]

## רכיב 2: גנרטור פוסטים עם Claude (Blog-Generator-Claude)

יש ריפו מוכן ב-Python בשם Blog-Generator-Claude שמתחבר ל-Anthropic API, מייצר outline לפוסט ולאחר מכן את הפוסט המלא על בסיס ההנחיות שאתה נותן.[^1]

הסקריפט מאפשר להגדיר נושא, מספר תתי-נושאים, אורך לכל סקשן, זהות הבלוגר, סגנון כתיבה ורשימת העדפות לשוניות, ושומר את התוצרים לקובצי טקסט או CSV.[^5][^1]

### למה הוא מתאים כ״מנוע כתיבה״ מאחורי הבלוג

- בנוי מראש סביב Claude 3 ו-Anthropic API, כולל שימוש בקובץ הנחיות ארוך שמגדיר קול, סגנון וקהל יעד – אידיאלי כדי להטמיע את ה-voice שלך כ-CPA & External CFO.[^1]
- מוציא outline + פוסט מלא, כך שקל לעבור לעבודה במבנה Markdown קבוע שמתאים לאסטרו.[^1]
- רישיון MIT וסקריפט יחיד, כך שקל לבצע fork ולהתאים אותו למבנה AstroPaper (frontmatter, slug, תגיות וכו').[^1]

## רכיב 3: השראה לאוטומציה מלאה – HowDoIUseAI

בפוסט "How I Built an Automated AI Blog in One Afternoon (With Claude ...)" מתואר בלוג אוטומטי שכותב את עצמו עם Claude Code, GitHub Actions ו-Claude API.[^4]

שם נבנתה תשתית ב-Next.js, שמריצה שלושה סקריפטים: fetch-videos.ts (מביא תמלולים מיוטיוב), generate-post.ts (שולח ל-Claude לכתיבת פוסט) ו-pipeline.ts (אורקסטרציה מלאה + מניעת כפילויות), עם GitHub Actions שדואג להרצה יומית ו-deploy ל-Vercel.[^4]

### מה לקחת משם לפרויקט שלך

- מודל חשיבה: צינור אוטומטי שמביא מקורות, מייצר פוסט, מבצע commit ומפעיל deploy – בלי מגע יד אדם.[^4]
- שימוש ב-GitHub Actions כ-cron חינמי להרצה יומית של סקריפט הגנרטור.[^4]
- עקרונות של ניטור כפילויות (קובץ JSON של "processed"), שאפשר ליישם גם אצלך אם תמשוך מקורות חיצוניים באופן אוטומטי.[^4]

## רכיב 4 (אופציונלי): Astro Blog Docker Template עם אוטומציה

קיים גם ריפו astro-blog-docker-template שמציע תבנית בלוג Astro מלאה עם Docker, כלי AI ואוטומציית deploy מובנית.[^6]

זהו בסיס טוב אם רוצים סטאק יותר "כבדה" ומוכנה לפרודקשן (כולל Docker-compose וכו') ואולי להכניס אליו בהמשך סקריפט גנרטור משלך או API פנימי.[^6]

## הצעת ארכיטקטורה קונקרטית עבורך

### 1. ריפו בלוג: Fork מ-AstroPaper

1. צור ריפו GitHub חדש מתוך התבנית satnaing/astro-paper (Use this template).[^3]
2. פרוס את האתר ב-Vercel או ב-GitHub Pages (ל-Astro יש תיעוד טוב לשניהם).[^7][^3]
3. ודא שתיקיית הפוסטים (למשל src/content/blog או דומה) ברורה, ותעדכן Frontmatter סטנדרטי: title, description, pubDate, tags, draft.

### 2. ריפו/תיקיית גנרטור: Fork מ-Blog-Generator-Claude

1. עשה fork ל-WonderingAboutAI/Blog-Generator-Claude או הוסף אותו כתיקיית /generator באותו מונורפו.[^1]
2. עדכן את הסקריפט כך שבמקום להוציא blog_post.txt בלבד, הוא יכתוב קובץ Markdown חדש בתוך תיקיית הפוסטים של AstroPaper, כולל Frontmatter.[^1]
3. שמור את ה-Anthropic API Key בקובץ .env או ב-GitHub Secrets (ANTHROPIC_API_KEY).[^4][^1]

### 3. מבנה קובץ פוסט טיפוסי

הסקריפט צריך ליצור קובץ בסגנון:

```markdown
---
title: "How AI Transforms FP&A"
description: "סקירה פרקטית על איך להשתמש ב-AI כדי לקצר סגירה חודשית ב-70%."
pubDate: 2026-04-06
tags: ["AI", "FP&A", "Finance Transformation"]
draft: false
---

תוכן הפוסט שנכתב על ידי Claude בעברית/אנגלית משולבת…
```

Frontmatter כזה משתלב טוב עם AstroPaper ותומך ב-SEO, תגיות וסינון.[^3]

### 4. אוטומציה עם GitHub Actions

בהשראת HowDoIUseAI, אפשר ליצור GitHub Action שירוץ פעם ביום/שבוע, יפעיל את סקריפט הגנרטור, יבצע commit ו-push לריפו, ויפעיל deploy אוטומטי.[^4]

השלבים ב-Workflow טיפוסי:

- checkout לקוד הבלוג
- התקנת Python ותלויות הגנרטור
- הרצת הסקריפט עם מפתח Anthropic מה-secrets
- אם נוצרו קבצים חדשים: git add, git commit, git push
- Vercel/GitHub Pages מבצעים build אוטומטי ומעלים את הבלוג

### 5. ניהול רעיונות ונושאים

אפשר להתחיל מבקשה ידנית: הסקריפט שואל אותך לנושא (למשל "AI ל-CFOs בישראל"), קהל יעד, מספר תתי-נושאים, וסגנון כתיבה, ומזין את זה ל-Claude יחד עם קובץ הנחיות שבו שמור ה-voice שלך.[^1]

בשלב הבא, בדומה ל-HowDoIUseAI, אפשר לחבר מקור רעיונות אוטומטי (למשל RSS, YouTube transcripts דרך Apify, פוסטים מלינקדאין שלך) ולהפוך אותם לחומר גלם לפוסטים.[^4]

## סקיל/תבניות נוספות שכדאי להכיר

- GitExtract מציע snapshot של קוד AstroPaper המוכן במיוחד לעבודה עם Claude ו-IDE מבוססי LLM, מה שמקל עליך להשתמש ב-Claude כדי לשנות את העיצוב/מבנה של התבנית.[^8]
- רשימת ה-Themes הרשמית של Astro מציגה עוד תבניות בלוג עם אינטגרציות ל-RSS, מניפסט ודברים נוספים – אם תרצה בעתיד לעבור לתבנית שמותאמת יותר ל-MD/MDX או ל-i18n.[^7]

## כיווני שיפור עתידיים

- שימוש ב-Claude Projects כדי להגדיר "Agent בלוג" שיודע לקבל תקציר/קובץ טרנסקריפט ולהוציא ישירות Markdown מותאם AstroPaper לפי מבנה קבוע.[^9]
- שילוב כלי Docker-Template כמו astro-blog-docker-template אם תרצה לעבור לסביבת הרצה מנוהלת עם CI/CD מלא ושילוב שירותי AI נוספים.[^6]
- הוספת לוגיקה של בקרת איכות – למשל PR אוטומטי במקום push ישיר, כדי שתוכל לעבור על כל פוסט לפני שהוא עולה לאוויר.

---

## References

1. [WonderingAboutAI/Blog-Generator-Claude - GitHub](https://github.com/WonderingAboutAI/Blog-Generator-Claude) - This Python script prompts Claude to first generate a blog outline and then a complete blog post bas...

2. [astro-paper/src/pages/rss.xml.ts at main - GitHub](https://github.com/satnaing/astro-paper/blob/main/src/pages/rss.xml.ts) - A minimal, accessible and SEO-friendly Astro blog theme - astro-paper/src/pages/rss.xml.ts at main ·...

3. [aadev777/astro-paper - GitHub](https://github.com/aadev777/astro-paper) - AstroPaper is a minimal, responsive, accessible and SEO-friendly Astro blog theme. This theme is des...

4. [How I Built an Automated AI Blog in One Afternoon (With Claude ...](https://nocodelife.com/how-we-built-howdoiuseai/) - A behind-the-scenes look at building HowDoIUseAI.com - a blog that writes itself using Claude Code, ...

5. [blog generator Claude v2.py - GitHub](https://github.com/WonderingAboutAI/Blog-Generator-Claude/blob/main/blog%20generator%20Claude%20v2.py) - This Python script prompts Claude to first generate a blog outline and then a complete blog post. Th...

6. [dougjaworski/astro-blog-docker-template - GitHub](https://github.com/dougjaworski/astro-blog-docker-template) - Complete Astro blog template with Docker, AI tools, and deployment automation. Built following the o...

7. [Themes | Astro](https://astro.build/themes/43/?search=&types%5B%5D=blog) - A minimal blog using Tailwind CSS and TypeScript. Integrated tags with filtering for posts by tags, ...

8. [Full Code of satnaing/astro-paper for AI | GitExtract](https://gitextract.com/satnaing/astro-paper) - Full source code of satnaing/astro-paper (93 files, 257.9 KB, 25 symbols) extracted for AI. Ready fo...

9. [קלוד פרוג'קטס (Claude Projects) - כלי פשוט ועוצמתי ליצירת סוכני AI יעילים](https://www.youtube.com/watch?v=8mWR1r28ia4) - בסרטון הזה תלמדו להכיר את קלוד פרוג'קטס (Claude Projects), כלי עוצמתי שיאפשר לכם ליצור סוכני AI מותא...

