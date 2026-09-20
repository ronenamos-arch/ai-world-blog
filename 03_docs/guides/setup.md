# מדריך התקנה

## דרישות מקדימות

- Node.js 20+
- Python 3.12+
- git
- API Keys: Anthropic, Firecrawl

## התקנת הבלוג (`blog/`)

```bash
cd blog
npm install
npm run dev
# localhost:4321
```

## התקנת הגנרטור (`generator/`)

```bash
cd generator
python -m venv .venv
source .venv/bin/activate    # Linux/Mac
# .venv\Scripts\activate     # Windows
pip install -e .
cp .env.example .env
# ערוך את .env עם המפתחות שלך
```

## הרצה ידנית של הצינור

```bash
cd generator
python -m src.cli --next                          # פריט הבא מהתור
python -m src.cli --url <URL> --type tool_explainer   # URL ספציפי
python -m src.cli --next --dry-run                    # בלי כתיבה לקובץ
```
