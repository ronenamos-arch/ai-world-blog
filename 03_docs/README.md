# עולם ה AI

בלוג עברית אוטומטי שמלמד על כלי AI חדשים — בהשראת [howdoiuseai.com](https://howdoiuseai.com), עם תוכן מקורי בעברית.

> **AI Agents & Developers:** Read [`CLAUDE.md`](CLAUDE.md) before making any changes. It contains critical rules that prevent deployment failures.
> See also: [`docs/deployment-lessons.md`](docs/deployment-lessons.md) — a log of real failures and how they were fixed.

## מבנה הפרויקט

```
.
├── blog/          אתר AstroPaper (Astro + Tailwind + TypeScript) — RTL עברית
├── generator/     צינור Python שמייצר פוסטים דרך Claude API + Firecrawl
└── docs/          תיעוד: התקנה, voice guide, pipeline
```

### `blog/` — אתר
- תבנית: [AstroPaper](https://github.com/satnaing/astro-paper)
- שפה: עברית (RTL native)
- Deploy: Vercel, אוטומטי מכל push ל-`main`
- פוסטים: `blog/src/data/blog/*.md`

### `generator/` — צינור ייצור
1. שולף URL מתור (`state/queue.yaml`)
2. Firecrawl גורד את המקור
3. Claude כותב פוסט מקורי בעברית (עיבוד, לא תרגום)
4. Self-review לאיכות
5. כותב `.md` עם `draft: true` לבלוג
6. מסמן ב-`state/processed.json`

**עקרון ליבה:** כל פוסט נכנס כ-`draft`. פרסום ידני בלבד.

## התחלה מהירה

ראה [docs/setup.md](docs/setup.md) למדריך התקנה מלא.

## שלבי הפרויקט

הצינור נבנה ב-10 שלבים, כל אחד עם smoke test משלו. ראה [תוכנית הפרויקט](../../../../.claude/plans/cozy-noodling-parnas.md).
