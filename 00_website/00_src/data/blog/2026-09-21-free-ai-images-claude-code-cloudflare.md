---
title: "איך לייצר תמונות AI בחינם ישירות מ-Claude Code עם Cloudflare"
description: "מדריך מעשי: חיבור Claude Code למודל FLUX.1 schnell דרך Cloudflare Workers AI להפקת כ-170 תמונות ביום בחינם וללא צורך במעבד גרפי."
pubDatetime: 2026-09-21T09:00:00+03:00
author: רואה חשבון רונן עמוס
tags:
  - Claude Code
  - Cloudflare
  - מחוללי תמונות
  - כלי AI
  - חיסכון בעלויות
featured: false
draft: false
ogImage: /images/posts/free-ai-images-claude-code-cloudflare.jpg
faqs:
  - question: "האם השירות באמת חינמי לתמיד או מדובר בתקופת ניסיון מוגבלת?"
    answer: "השירות חינמי לחלוטין. חברת Cloudflare מעניקה לכל חשבון מכסה יומית קבועה של 10,000 נוירונים (Neurons) ללא עלות, המתאפסת בכל יממה מחדש ללא תאריך תפוגה וללא צורך בהזנת כרטיס אשראי."
  - question: "כמה תמונות ביום ניתן לייצר במסגרת המכסה החינמית?"
    answer: "כ-173 תמונות ביממה בהגדרות ברירת המחדל (ברזולוציית 1024x1024 ו-4 צעדי דיפוזיה). כל תמונה כזו צורכת 57.6 נוירונים בלבד."
  - question: "האם מותר להשתמש בתמונות שנוצרו לשימוש מסחרי?"
    answer: "כן. המודל FLUX.1 schnell מבית Black Forest Labs שוחרר תחת רישיון קוד פתוח Apache 2.0, המאפשר שימוש מסחרי חופשי לחלוטין עבור אתרים, בלוגים, פוסטים ומוצרים דיגיטליים."
  - question: "האם צריך להרים שרת או לקודד Cloudflare Worker בענן?"
    answer: "לא. הגישה למודל מתבצעת ישירות באמצעות REST API סטנדרטי. הסקריפט שולח בקשת HTTPS יחידה עם מפתח ה-API ומקבל בחזרה את קובץ התמונה המוכן."
---

יוצרי תוכן, בוני אתרים ומפתחים מוצאים את עצמם משלמים עשרות דולרים בכל חודש למחוללי תמונות כמו Midjourney או מנויי DALL-E, רק כדי לייצר תמונות נושא לפוסטים, גרפיקות רקע או מוקאפים מהירים. מעבר לעלות המצטברת, הצורך לקטוע את רצף העבודה בטרמינל, לעבור לממשק דפדפן, להמתין בתור ולהוריד קבצים ידנית יוצר צוואר בקבוק מיותר ומאט את קצב הפיתוח.

**הפתרון האלגנטי והחסכוני ביותר הוא הפיכת Claude Code למחולל תמונות עצמאי הפועל ישירות משורת הפקודה, באמצעות חיבורו למודל FLUX.1 schnell הרץ על גבי תשתית Cloudflare Workers AI.** אתם מתארים את התמונה במילים פשוטות באנגלית, Claude מתרגם את הבקשה לפרומפט אופטימלי, מפעיל סקריפט קצר ושומר קובץ JPG מוכן בתיקיית הפרויקט – והכל במסגרת מכסה יומית של כ-173 תמונות בחינם לחלוטין, ללא צורך בכרטיס מסך ייעודי.

<div class="rounded-2xl border border-accent/30 bg-accent/5 p-6 my-8 shadow-sm">
<div class="text-base font-bold text-foreground mb-4">⚡ תמונת מצב: מחוללי תמונות בתשלום מול צינור Claude Code ו-Cloudflare</div>
<div class="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm">
<div class="border-b md:border-b-0 md:border-l border-border/60 pb-4 md:pb-0 md:pl-6">
<div class="font-bold text-accent mb-1">1. עלות חודשית ושנתית</div>
<div class="text-muted-foreground text-xs leading-relaxed"><strong>מנויים בתשלום:</strong> 30$ עד 60$ בחודש (מעל 360$ בשנה).<br><strong class="text-emerald-500 font-semibold">Cloudflare + Claude:</strong> 0$ לחלוטין במסגרת מכסת 10,000 נוירונים יומית קבועה.</div>
</div>
<div class="border-b md:border-b-0 md:border-l border-border/60 pb-4 md:pb-0 md:pl-6">
<div class="font-bold text-accent mb-1">2. ממשק וזרימת עבודה</div>
<div class="text-muted-foreground text-xs leading-relaxed"><strong>מסורתי:</strong> מעבר לדפדפן, כתיבת פרומפטים ידנית והורדת קבצים.<br><strong class="text-accent font-semibold">סקיל טרמינל:</strong> פקודה טקסטואלית יחידה בקונסול שומרת קובץ ישירות בנתיב היעד.</div>
</div>
<div>
<div class="font-bold text-accent mb-1">3. רישוי מסחרי</div>
<div class="text-muted-foreground text-xs leading-relaxed"><strong>שירותים סגורים:</strong> תלוי ברמת המנוי ומגבלות שימוש.<br><strong class="text-emerald-500 font-semibold">FLUX.1 schnell:</strong> רישיון פתוח מלא Apache 2.0 לכל שימוש מסחרי.</div>
</div>
</div>
</div>

---

## איך זה עובד? ארכיטקטורת המערכת

הצינור כולו מורכב משלושה חלקים שעובדים בסינרגיה מושלמת:

![תרשים זרימת תהליך ייצור התמונה: מהטרמינל ועד לקובץ ה-JPG הסופי](/images/posts/cloudflare-workers-ai-workflow.jpg)

<div class="grid grid-cols-1 md:grid-cols-3 gap-4 my-6">
<div class="p-5 rounded-xl border border-border bg-card shadow-sm">
<div class="flex items-center gap-2 mb-2">
<span class="w-7 h-7 rounded-lg bg-accent/20 text-accent font-bold flex items-center justify-center text-xs">1</span>
<span class="font-bold text-sm text-foreground">FLUX.1 schnell</span>
</div>
<p class="text-xs text-muted-foreground leading-relaxed">מודל קוד פתוח מהיר מבית Black Forest Labs, המייצר תמונות חדות ומדויקות ב-4 צעדי דיפוזיה בלבד ללא עומס חישובי מיותר.</p>
</div>

<div class="p-5 rounded-xl border border-border bg-card shadow-sm">
<div class="flex items-center gap-2 mb-2">
<span class="w-7 h-7 rounded-lg bg-orange-500/20 text-orange-400 font-bold flex items-center justify-center text-xs">2</span>
<span class="font-bold text-sm text-foreground">Workers AI</span>
</div>
<p class="text-xs text-muted-foreground leading-relaxed">רשת שרתי ה-GPU של Cloudflare המריצה את המודל ומנגישה אותו ב-REST API פשוט, עם מכסה קבועה של 10,000 נוירונים חינם ביום.</p>
</div>

<div class="p-5 rounded-xl border border-border bg-card shadow-sm">
<div class="flex items-center gap-2 mb-2">
<span class="w-7 h-7 rounded-lg bg-emerald-500/20 text-emerald-400 font-bold flex items-center justify-center text-xs">3</span>
<span class="font-bold text-sm text-foreground">Claude Skill</span>
</div>
<p class="text-xs text-muted-foreground leading-relaxed">המוח בטרמינל: Claude מקבל בקשה פשוטה, הופך אותה לפרומפט אומנותי מורחב, מפעיל את הסקריפט ושומר את ה-JPG בתיקייה.</p>
</div>
</div>

### חישוב המכסה: מתמטיקת ה-Neurons של Cloudflare

Cloudflare מודדת את צריכת המשאבים ביחידות חישוב הנקראות **Neurons**. הנה פירוק העלויות והחישוב המדויק:

<div class="overflow-x-auto my-6 rounded-xl border border-border bg-card shadow-sm">
<table class="w-full text-sm text-right border-collapse">
<thead>
<tr class="border-b border-border bg-muted/50 text-foreground font-semibold">
<th class="p-3.5">פעולה / רכיב</th>
<th class="p-3.5">עלות בנוירונים (Neurons)</th>
<th class="p-3.5">משמעות מעשית</th>
</tr>
</thead>
<tbody class="divide-y divide-border/60 text-muted-foreground text-xs">
<tr>
<td class="p-3.5 font-medium text-foreground">מכסה יומית חינמית (כל חשבון)</td>
<td class="p-3.5 font-bold text-emerald-500">10,000 נוירונים / יום</td>
<td class="p-3.5">מתאפסת בכל 24 שעות באופן אוטומטי</td>
</tr>
<tr>
<td class="p-3.5 font-medium text-foreground">צעד דיפוזיה בודד (Diffusion Step)</td>
<td class="p-3.5 font-mono">9.6 נוירונים</td>
<td class="p-3.5">מעבר חידוד של המודל על התמונה</td>
</tr>
<tr>
<td class="p-3.5 font-medium text-foreground">אריח פלט בודד (512x512)</td>
<td class="p-3.5 font-mono">4.8 נוירונים</td>
<td class="p-3.5">יחידת שטח של התמונה המרונדרת</td>
</tr>
<tr class="bg-accent/5 font-semibold text-foreground">
<td class="p-3.5 text-accent">תמונת ברירת מחדל (1024x1024, 4 צעדים)</td>
<td class="p-3.5 font-mono text-accent">57.6 נוירונים</td>
<td class="p-3.5 font-bold text-accent">4 אריחים + 4 צעדים = 57.6 בלבד</td>
</tr>
<tr class="bg-emerald-500/5 font-semibold text-foreground">
<td class="p-3.5 text-emerald-500">סך תמונות חינם ביממה (ברירת מחדל)</td>
<td class="p-3.5 font-bold text-emerald-500 text-sm">~173 תמונות בכל יום</td>
<td class="p-3.5 text-emerald-600 dark:text-emerald-400">מעל 5,000 תמונות חינמיות בחודש</td>
</tr>
<tr>
<td class="p-3.5 font-medium text-foreground">תמונות ברמת איכות מוגברת (8 צעדים)</td>
<td class="p-3.5 font-mono">96.0 נוירונים</td>
<td class="p-3.5">כ-104 תמונות חינם בכל יום</td>
</tr>
</tbody>
</table>
</div>

---

## שלב 1: השגת מפתחות הגישה מ-Cloudflare

כדי לתקשר עם ה-API של Cloudflare תזדקקו לשני נתונים בלבד מחשבון החינם שלכם: **Account ID** ו-**API Token**.

<div class="space-y-3 my-6">
<div class="flex items-start gap-3 p-4 rounded-xl border border-border bg-card">
<span class="w-6 h-6 rounded-full bg-accent text-white flex items-center justify-center text-xs font-bold shrink-0 mt-0.5">1</span>
<div class="text-xs text-muted-foreground leading-relaxed">היכנסו ללוח הבקרה בכתובת <a href="https://dash.cloudflare.com/" target="_blank" rel="noopener" class="text-accent underline font-semibold">dash.cloudflare.com</a> (פתיחת חשבון חינמית לחלוטין ללא כרטיס אשראי).</div>
</div>

<div class="flex items-start gap-3 p-4 rounded-xl border border-border bg-card">
<span class="w-6 h-6 rounded-full bg-accent text-white flex items-center justify-center text-xs font-bold shrink-0 mt-0.5">2</span>
<div class="text-xs text-muted-foreground leading-relaxed">בתפריט הצד השמאלי גשו אל <strong>AI &rarr; Workers AI</strong> ולחצו על כפתור <strong>Use REST API</strong>.</div>
</div>

<div class="flex items-start gap-3 p-4 rounded-xl border border-border bg-card">
<span class="w-6 h-6 rounded-full bg-accent text-white flex items-center justify-center text-xs font-bold shrink-0 mt-0.5">3</span>
<div class="text-xs text-muted-foreground leading-relaxed">לחצו על <strong>Create a Workers AI API Token</strong>. המערכת תכין עבורכם תבנית מוכנה עם הרשאות קריאה ועריכה. אשרו והעתיקו את הטוקן ואת ה-<strong>Account ID</strong>.</div>
</div>
</div>

<div class="border-r-4 border-amber-500 bg-amber-500/10 p-4 rounded-l-xl my-6">
<div class="font-bold text-amber-500 text-sm mb-1">⚠️ אבטחת מפתח ה-API:</div>
<div class="text-xs text-amber-200/90 leading-relaxed">הטוקן של Cloudflare משמש כסיסמה למכסת ה-AI שלכם. שמרו אותו אך ורק בקובץ <code>.env</code> מקומי וודאו שהוא מופיע בקובץ <code>.gitignore</code> כדי שלא ידלוף ל-GitHub.</div>
</div>

---

## שלב 2: הגדרת הסקיל ב-Claude Code

סקיל ב-Claude Code הוא בסך הכל תיקייה הממוקמת תחת נתיב הסקילים ומכילה קובץ הנחיות `SKILL.md` לצד סקריפט ביצוע.

צרו תיקייה בשם `.claude/skills/cf-image/` ובתוכה הניחו שני קבצים:

### 1. קובץ הביצוע `generate.py`
הסקריפט שולח קריאת HTTP בודדת לשרתי Cloudflare, מקבל את התמונה המקודדת ב-Base64 ושומר אותה כקובץ מקומי:

```python
import os
import sys
import argparse
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

ACCOUNT_ID = os.getenv("CF_ACCOUNT_ID")
API_TOKEN = os.getenv("CF_API_TOKEN")
MODEL = "@cf/black-forest-labs/flux-1-schnell"

parser = argparse.ArgumentParser(description="Generate image via Cloudflare Workers AI")
parser.add_argument("--prompt", required=True, help="Prompt text for Flux")
parser.add_argument("--output", default="output.jpg", help="Output file path")
parser.add_argument("--steps", type=int, default=4, help="Diffusion steps (default 4)")
args = parser.parse_args()

url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/{MODEL}"
headers = {"Authorization": f"Bearer {API_TOKEN}"}
payload = {"prompt": args.prompt, "steps": args.steps}

response = requests.post(url, headers=headers, json=payload)
data = response.json()

if "result" in data and "image" in data["result"]:
    img_bytes = base64.b64decode(data["result"]["image"])
    with open(args.output, "wb") as f:
        f.write(img_bytes)
    print(f"Saved {args.output}")
else:
    print(f"Error: {data}")
    sys.exit(1)
```

### 2. קובץ ההוראות `SKILL.md`
קובץ זה מסביר ל-Claude מתי להפעיל את הסקיל וכיצד לבנות פרומפט עשיר עבור Flux:

```markdown
---
name: cf-image
description: Generate free AI images using Cloudflare Workers AI (flux-1-schnell model). Use whenever the user asks for an image, photo, illustration, or graphic.
---

When the user asks for an image:
1. Expand the idea into a detailed Flux prompt containing: subject, artistic style, framing/composition, lighting and mood, color palette.
2. Run generate.py with --prompt "<detailed_prompt>" --output "<filename>.jpg" --steps 4.
3. Confirm file creation and display the path to the user.
```

<div class="rounded-xl border border-border bg-card p-5 my-6">
<div class="font-bold text-sm text-foreground mb-2">📦 התקנת תלויות והגדרת הסביבה:</div>
<p class="text-xs text-muted-foreground mb-3">התקינו את שתי הספריות הנדרשות לשורש הפרויקט:</p>
<pre class="bg-zinc-900 border border-zinc-800 text-zinc-100 p-3.5 rounded-xl text-xs font-mono overflow-x-auto shadow-inner">pip install requests python-dotenv</pre>
<p class="text-xs text-muted-foreground my-2">והדביקו את המפתחות שלכם לקובץ <code>.env</code>:</p>
<pre class="bg-zinc-900 border border-zinc-800 text-zinc-100 p-3.5 rounded-xl text-xs font-mono overflow-x-auto shadow-inner">CF_ACCOUNT_ID=your_account_id_here
CF_API_TOKEN=your_api_token_here</pre>
</div>

---

## שלב 3: הפקת תמונות מתוך שיחת טרמינל

כעת פתחו את Claude Code בטרמינל ובקשו תמונה בשפה חופשית ופשוטה:

```bash
make me a picture of a cyberpunk cat coding at night
```

<div class="border-r-4 border-accent bg-accent/5 p-5 rounded-l-xl my-6">
<div class="font-bold text-accent text-sm mb-2">🔄 מה קורה מאחורי הקלעים תוך 3 שניות?</div>
<ul class="text-xs text-muted-foreground space-y-2 leading-relaxed">
<li><strong>1. הנדסת פרומפט אוטומטית:</strong> Claude מרחיב את 6 המילים שלכם לפרומפט קולנועי עשיר: <code>close-up of a fluffy tabby cat wearing tiny neon-rimmed glasses in front of a glowing laptop, dark room lit by pink and cyan neon signs, rain-streaked window, cinematic photo, shallow depth of field</code>.</li>
<li><strong>2. שיגור בקשה מהירה:</strong> הסקריפט שולח את הפרומפט לענן של Cloudflare.</li>
<li><strong>3. קבלת קובץ מוכן:</strong> קובץ ה-JPG נחת ישירות בתיקיית הפרויקט מוכן להטמעה.</li>
</ul>
</div>

---

## כללי זהב לכתיבת פרומפטים ב-FLUX.1 schnell

<div class="grid grid-cols-1 md:grid-cols-2 gap-4 my-6">
<div class="p-5 rounded-xl border border-border bg-card shadow-sm">
<div class="font-bold text-sm text-accent mb-2">🎯 4 צעדים זה שביל הזהב</div>
<p class="text-xs text-muted-foreground leading-relaxed">המודל אופטימיזלי למהירות והתכנסות מהירה. 4 צעדי דיפוזיה מפיקים תוצאה מצוינת. העלאה ל-16 צעדים רק תבזבז נוירונים ללא שיפור ניכר.</p>
</div>

<div class="p-5 rounded-xl border border-border bg-card shadow-sm">
<div class="font-bold text-sm text-rose-400 mb-2">🚫 אל תבקשו טקסט בתוך התמונה</div>
<p class="text-xs text-muted-foreground leading-relaxed">מודל schnell אינו מרנדר אותיות ומילים קריאות. בקשו את הגרפיקה הנקייה והוסיפו טקסטים, לוגואים וכותרות לאחר מכן בעזרת קוד או עיצוב.</p>
</div>

<div class="p-5 rounded-xl border border-border bg-card shadow-sm">
<div class="font-bold text-sm text-emerald-400 mb-2">🎨 5 מרכיבי יסוד בכל בקשה</div>
<p class="text-xs text-muted-foreground leading-relaxed">הקפידו לכלול: נושא ברור (Subject), סגנון אומנותי (Style), קומפוזיציה וזווית (Composition), תאורה ואווירה (Lighting), ופלטת צבעים (Palette).</p>
</div>

<div class="p-5 rounded-xl border border-border bg-card shadow-sm">
<div class="font-bold text-sm text-amber-400 mb-2">📝 פסקאות עדיפות על רשימת תגיות</div>
<p class="text-xs text-muted-foreground leading-relaxed">FLUX.1 מבין שפה טבעית היטב. משפט תיאורי עשיר ומגובש יפיק תוצאה מדויקת בהרבה ממחרוזת ארוכה של מילות מפתח מופרדות בפסיקים.</p>
</div>
</div>

---

## למי מתאים הפתרון ולמה הוא כל כך יעיל?

<div class="grid grid-cols-1 md:grid-cols-2 gap-6 my-6">
<div class="p-6 rounded-2xl border border-border bg-card">
<div class="font-bold text-base text-foreground mb-3">👥 למי זה מתאים?</div>
<ul class="text-xs text-muted-foreground space-y-2.5 leading-relaxed">
<li>• <strong>מפתחים ובוני אתרים:</strong> הזקוקים לתמונות רקע, אייקונים ומוקאפים מבלי לעזוב את ה-IDE.</li>
<li>• <strong>בלוגרים ויוצרי תוכן:</strong> המעוניינים בתמונות נושא (Hero Images) ייחודיות באפס עלות.</li>
<li>• <strong>בוני סוכני AI:</strong> המעוניינים לשלב מודול יצירת תמונות אוטונומי בצינורות עבודה ללא עלויות API.</li>
</ul>
</div>

<div class="p-6 rounded-2xl border border-border bg-card">
<div class="font-bold text-base text-foreground mb-3">💡 למה זה כדאי?</div>
<ul class="text-xs text-muted-foreground space-y-2.5 leading-relaxed">
<li>• <strong class="text-emerald-500">חיסכון של מאות דולרים:</strong> אפס הוצאות על מנויי צד-ג' כבדים.</li>
<li>• <strong class="text-accent">מהירות עבודה:</strong> תמונה בדיסק תוך שניות ישירות משורת הפקודה.</li>
<li>• <strong class="text-foreground">רישיון מסחרי מלא:</strong> שימוש חופשי לחלוטין לפי רישיון Apache 2.0.</li>
</ul>
</div>
</div>

---

<div class="rounded-2xl border border-accent/30 bg-gradient-to-r from-accent/15 via-accent/5 to-transparent p-6 my-8 shadow-sm">
<div class="font-bold text-base text-foreground mb-2">🚀 סיכום והמלצה מעשית</div>
<p class="text-xs text-muted-foreground leading-relaxed">
החיבור בין יכולות ניהול השיחה של Claude Code לכוח המחשוב החינמי של Cloudflare Workers AI מדגים את העוצמה של סוכני AI מודרניים: פתרון בעיות קצה מהיר, אלגנטי ובאפס עלות. הגדירו את הסקיל פעם אחת בפרויקט שלכם, ותיהנו ממחולל תמונות אמין של כ-170 תמונות ביום בכל פיתוח עתידי.
</p>
</div>

---

<div class="my-10 not-prose">
<div class="mb-4">
<h3 class="text-xl font-bold text-foreground">מדריכים נוספים שאולי יעניינו אותך:</h3>
<p class="text-sm text-muted-foreground mt-1">הרחיבו את ארגז הכלים שלכם עם המדריכים המובילים באתר:</p>
</div>
<div class="grid grid-cols-1 md:grid-cols-3 gap-6">

<a href="/posts/2026-09-22-jev-ai-model-vercel-gateway-guide" class="group flex flex-col overflow-hidden rounded-2xl border border-border/80 bg-card transition-all duration-300 hover:-translate-y-1 hover:border-accent/60 hover:shadow-lg no-underline">
<div class="aspect-video w-full overflow-hidden bg-muted">
<img src="/images/posts/jev-ai-model-vercel-gateway-guide.png" alt="מדריך Jev AI ומודל System-1" class="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105 m-0 border-0" />
</div>
<div class="flex flex-1 flex-col p-4">
<span class="text-xs font-bold text-accent mb-1">חדש · ארכיטקטורת AI</span>
<h4 class="text-base font-bold text-foreground group-hover:text-accent transition-colors m-0 leading-snug">מדריך מעשי ל-Jev AI: מה זה מודל System-1 ולמה זה יחסוך 85% בעלויות</h4>
<p class="text-xs text-muted-foreground mt-2 line-clamp-2 leading-relaxed">מנוע קבלת החלטות סופר-מהיר ב-15ms, חיבור ל-Vercel AI Gateway ואוטומציות חכמות.</p>
<span class="mt-auto pt-3 text-xs font-semibold text-accent flex items-center gap-1">לקריאת המדריך &larr;</span>
</div>
</a>

<a href="/posts/2026-09-21-how-to-edit-videos-with-claude-code" class="group flex flex-col overflow-hidden rounded-2xl border border-border/80 bg-card transition-all duration-300 hover:-translate-y-1 hover:border-accent/60 hover:shadow-lg no-underline">
<div class="aspect-video w-full overflow-hidden bg-muted">
<img src="/images/posts/how-to-edit-videos-with-claude-code.jpg" alt="עריכת סרטונים עם Claude Code" class="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105 m-0 border-0" />
</div>
<div class="flex flex-1 flex-col p-4">
<span class="text-xs font-bold text-accent mb-1">מדריך מעשי ליוצרי תוכן</span>
<h4 class="text-base font-bold text-foreground group-hover:text-accent transition-colors m-0 leading-snug">איך לערוך סרטוני יוטיוב מלאים עם Claude Code: מדריך ללא עורך וידאו</h4>
<p class="text-xs text-muted-foreground mt-2 line-clamp-2 leading-relaxed">חיתוך שתיקות, הוספת אנימציות Remotion ושיפור סאונד אוטומטי מתוך הטרמינל.</p>
<span class="mt-auto pt-3 text-xs font-semibold text-accent flex items-center gap-1">לקריאת המדריך &larr;</span>
</div>
</a>

<a href="/posts/2026-09-16-google-ai-pro-deal" class="group flex flex-col overflow-hidden rounded-2xl border border-border/80 bg-card transition-all duration-300 hover:-translate-y-1 hover:border-accent/60 hover:shadow-lg no-underline">
<div class="aspect-video w-full overflow-hidden bg-muted">
<img src="/images/posts/google-ai-pro-deal.jpg" alt="Gemini ואוטומציות מתקדמות" class="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105 m-0 border-0" />
</div>
<div class="flex flex-1 flex-col p-4">
<span class="text-xs font-bold text-emerald-500 mb-1">פרודוקטיביות וכלים</span>
<h4 class="text-base font-bold text-foreground group-hover:text-accent transition-colors m-0 leading-snug">Gemini ואוטומציות: איך להפוך את עוזר ה-AI למנוע עבודה אוטונומי</h4>
<p class="text-xs text-muted-foreground mt-2 line-clamp-2 leading-relaxed">שילוב סוכני Deep Research, מחקר ב-NotebookLM והטמעה מלאה ב-Google Workspace.</p>
<span class="mt-auto pt-3 text-xs font-semibold text-accent flex items-center gap-1">לקריאת המדריך &larr;</span>
</div>
</a>

</div>
</div>
