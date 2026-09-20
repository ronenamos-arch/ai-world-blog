from notion_client import Client
import os, glob, re, json

client = Client(auth=os.getenv('NOTION_TOKEN'))
res = client.search(filter={'property': 'object', 'value': 'page'})
results = res.get('results', [])

md_files = glob.glob('blog/src/data/blog/*.md')
md_data = {}
for mf in md_files:
    slug = os.path.basename(mf).replace('.md', '')
    with open(mf, 'r', encoding='utf-8') as f:
        content = f.read()
    title_match = re.search(r'title:\s*["\x27]?(.*?)["\x27]?\s*\n', content)
    desc_match = re.search(r'description:\s*["\x27]?(.*?)["\x27]?\s*\n', content)
    title = title_match.group(1) if title_match else ''
    desc = desc_match.group(1) if desc_match else ''
    md_data[slug] = {
        'path': mf,
        'title': title,
        'desc': desc,
        'slug': slug,
        'content': content
    }

mapping = {
    "חיבור קלוד לseo": "seo-reports",
    "Agent Loop ב‑Claude: המדריך המעשי לבניית סוכן יציב": "agent-loop",
    "וורד פרס קלאוד ביחד יצירת מכונת תוכן": "wordpress-claude",
    "GitHub Copilot CLI: המדריך המעשי לעבוד עם AI מהטרמינל": "2026-04-14-github-for-beginners", # or copilot
    "גוגל אוטומציה": "2026-04-21-google-chrome-skills-ai-automation",
    "claude": "claude-practices",
    "Gemini API חינמי: המדריך המעשי להתחלה עם Google AI Studio": "2026-04-21-gemini-api-free-google-ai-studio-guide",
    "Agent harness": "2026-07-07-harness-memory",
    "יצירת תמונות עם AI — מדריך למתחיל: Midjourney, DALL·E ו-Ideogram": "2026-04-12-7-powerful-ai-design-tools-creators-are-using-in-2026-to-sav", # or design tools
    "AI שקורא מסמכים במקומכם: איך לסכם, לנתח ולחלץ מידע מ-PDF בשניות": "2026-04-09-6-free-ai-research-tools",
    "כתיבה עם AI שנשמעת כמוכם — לא כמו רובוט": "2026-04-16-creating-content-claude",
    "NotebookLM overview": "2026-04-09-6-free-ai-research-tools",
    "מקליט, מתמלל ומסכם: כלי AI לניהול פגישות שישנו את הדרך שאתם עובדים": "2026-04-13-ai-meeting-tools",
    "Claude Managed Agents: המדריך המעשי לסוכנים מנוהלים ב‑2026": "2026-04-21-claude-managed-agents-practical-guide-2026",
    "Resend Automations: המדריך המעשי לאימיילים אוטומטיים חכמים": "2026-04-21-resend-automations-lifecycle-email-guide",
    "AI Agents Are Changing Business: 10 Platforms You Need on Your Radar": "2026-04-21-ai-agents-platforms-business-2026-guide",
    "10 גיטהאב לשלוט בקלוד קוד": "2026-07-07-github-claude",
    "סוכן בגיטהאב": "2026-04-21-ai-agents-github-squad-guide-2026",
    "איך אני משפר את קלוד שלי עם הזמן": "2026-07-07-claude-improve",
    "7 פקודות לקלוד לחסכון הטוקנים": "2026-07-07-reduce-claude-code-token-usage",
    "שירותי גוגל כתחליף לקלוד": "2026-07-07-claude-google-ai-pro-antigravity",
    "יצירת תוכן עם קלוד": "2026-04-16-creating-content-claude",
    "סוכן always on ב vercel": "2026-04-14-agent-always-on-vercel",
    "גיטהאב למתחילים": "2026-04-14-github-for-beginners",
    "API חשובים לחיפוש": "2026-04-13-7-free-web-apis-every-developer-and-vibe-coder-should-know",
    "business ideas": "2026-04-13-webwave"
}

print("Mapping verification:")
for k, v in mapping.items():
    exists = v in md_data
    print(f"[{'OK' if exists else 'MISSING'}] '{k}' -> {v}")
