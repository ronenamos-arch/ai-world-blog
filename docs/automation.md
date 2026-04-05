# תיעוד ה-Pipeline

## זרימה

```
queue.yaml → firecrawl → claude (outline → post → review) → markdown → processed.json
```

## Run modes

| פקודה | מה קורה |
|---|---|
| `python -m src.cli --next` | שולף פריט הבא מהתור, מריץ צינור, כותב קובץ |
| `python -m src.cli --url <URL> --type <type>` | רץ על URL ספציפי |
| `python -m src.cli --next --dry-run` | רץ בלי לכתוב (debug) |
| `python -m src.cli --next --no-dedup` | מדלג על בדיקת processed |

## סוגי פוסטים

| `--type` | מטרה |
|---|---|
| `tool_explainer` | מה זה X ואיך משתמשים בו |
| `tutorial` | איך לעשות X עם Y |
| `comparison` | X מול Y — מה עדיף |
| `use_case` | איך להשתמש ב-AI ל-X |

## GitHub Actions

ראה `.github/workflows/generate-post.yml`. 
- Manual: `workflow_dispatch` מה-UI.
- Scheduled: cron יומי ב-07:00 UTC (10:00 בארץ).

**כל פוסט נשמר כ-`draft: true`**. פרסום = שינוי ידני ל-`draft: false` + push.

## State files

- `state/queue.yaml` — רשימת URLs ממתינים
- `state/processed.json` — מה שכבר נכתב (למניעת כפילויות)
