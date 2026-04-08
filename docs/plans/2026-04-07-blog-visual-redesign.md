# עיצוב ויזואלי — עולם ה AI

## החלטות

- **צבעים:** indigo/lavender (`#4f46e5` light, `#818cf8` dark)
- **Hero:** תמונת Unsplash קבועה + overlay gradient כהה + טקסט לבן
- **כרטיסים:** תמונה 16:9 מעל הכותרת, fallback gradient
- **פוסט:** ogImage כ-hero image בראש העמוד

## קבצים שישתנו

1. `blog/src/styles/global.css` — צבעים
2. `blog/src/components/Card.astro` — תמונה בכרטיס
3. `blog/src/pages/index.astro` — hero עם רקע
4. `blog/src/layouts/PostDetails.astro` — hero image בפוסט
5. `blog/public/hero-bg.jpg` — תמונת רקע קבועה

## Playwright

- `blog/tests/visual.spec.ts` — screenshot homepage + post
- תוצאות ב-`blog/tests/screenshots/`
