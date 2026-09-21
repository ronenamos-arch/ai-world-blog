---
title: "איך לערוך סרטוני יוטיוב מלאים עם Claude Code: מדריך מעשי ללא עורך וידאו"
description: "מדריך מקיף לעריכת וידאו אוטונומית עם Claude Code: חיתוך שתיקות, יצירת אנימציות Remotion, ניקוי רעשי קול ואפקטים קוליים ישירות מהטרמינל."
pubDatetime: 2026-09-21T09:30:00+03:00
author: רואה חשבון רונן עמוס
tags:
  - Claude Code
  - יוטיוב
  - עריכת וידאו
  - אוטומציה
  - Remotion
featured: false
draft: false
ogImage: /images/posts/how-to-edit-videos-with-claude-code.jpg
faqs:
  - question: "האם חייבים לדעת לתכנת או להבין בעריכת וידאו כדי להשתמש במערכת?"
    answer: "ממש לא. אתם מתקשרים עם Claude Code בשפה טבעית ופשוטה. התפקיד שלכם מתמצה בהקלטת עצמכם מדברים והפעלת פקודות טקסטואליות בטרמינל. Claude Code מנהל את כלי העריכה והקוד מאחורי הקלעים."
  - question: "האם ניתן להפעיל את התהליך ללא עלויות נוספות?"
    answer: "כן, שלב החיתוך המרכזי מתבצע על גבי המכסה החינמית של AssemblyAI, ושלב ניקוי הסאונד כולל מנוע מקומי מבוסס RNNoise שרץ על המחשב שלכם ללא צורך במפתח API בתשלום."
  - question: "האם צריך לצלם את מסך המחשב בנפרד במהלך ההקלטה?"
    answer: "לא. המערכת מייצרת הדגמות מסך, דיאגרמות ואנימציות שלמות בעזרת קוד Remotion. אתם מקליטים רק את עצמכם מדברים, וכל שאר האלמנטים הוויזואליים נבנים אוטומטית."
  - question: "האם המערכת עובדת על Windows, Mac ו-Linux?"
    answer: "כן. כל הרכיבים (Python, Node.js, FFmpeg ו-Claude Code) הינם חוצי-פלטפורמות מלאים ופועלים בצורה זהה בכל מערכות ההפעלה."
---

עריכת וידאו איכותית ליוטיוב היא כנראה המחסום הגדול ביותר שניצב בפני יוצרי תוכן, בעלי עסקים ומפתחים. חיתוך שתיקות וטעויות דיבור, עיצוב אלמנטים גרפיים מונפשים על המסך, בידוד רעשי רקע והתאמת אפקטים קוליים (SFX) על כל הדגשה דורשים בין 5 ל-10 שעות עבודה מתישה לכל סרטון בודד בתוכנות עריכה כבדות כמו Premiere או DaVinci Resolve. עבור רובנו, הזמן והמורכבות הזו הופכים את הפקת הווידאו למעמסה בלתי אפשרית.

**המהפכה האמיתית מתרחשת כשהופכים את Claude Code לעורך הווידאו האוטונומי שלכם ישירות מהטרמינל: אתם מקליטים את עצמכם מדברים ברצף ללא חשש מטעויות, זורקים קובץ וידאו יחיד לתיקייה, וסדרת סקילים מבוססי AI חותכת את הפספוסים, מרנדרת אנימציות React מרהיבות ב-Remotion, מסננת רעשים ומדביקה סאונד מתוזמן.**

<div class="rounded-2xl border border-accent/30 bg-accent/5 p-6 my-8 shadow-sm">
<div class="text-base font-bold text-foreground mb-4">🎬 השוואה ישירה: עריכת וידאו מסורתית מול צינור העריכה של Claude Code</div>
<div class="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm">
<div class="border-b md:border-b-0 md:border-l border-border/60 pb-4 md:pb-0 md:pl-6">
<div class="font-bold text-accent mb-1">1. השקעת זמן ומאמץ</div>
<div class="text-muted-foreground text-xs leading-relaxed"><strong>עריכה ידנית:</strong> 6 עד 10 שעות מול ציר זמן, חיתוך ידני של כל טייק.<br><strong class="text-emerald-500 font-semibold">Claude Code:</strong> כ-15 דקות של הנחיות טקסטואליות פשוטות בטרמינל.</div>
</div>
<div class="border-b md:border-b-0 md:border-l border-border/60 pb-4 md:pb-0 md:pl-6">
<div class="font-bold text-accent mb-1">2. גרפיקה והנפשות מסך</div>
<div class="text-muted-foreground text-xs leading-relaxed"><strong>תוכנות עריכה:</strong> טמפלייטים יקרים, שכבות מורכבות ומסגרות מפתח.<br><strong class="text-accent font-semibold">Remotion + Claude:</strong> הפקת אנימציות קוד React מסונכרנות בדיוק למילים.</div>
</div>
<div>
<div class="font-bold text-accent mb-1">3. עקומת למידה</div>
<div class="text-muted-foreground text-xs leading-relaxed"><strong>מסורתי:</strong> לימוד ממשקי עריכה עמוסים ותוכנות סאונד נפרדות.<br><strong class="text-emerald-500 font-semibold">סקילים בטרמינל:</strong> 6 משפטים פשוטים באנגלית שמכוונים סוכנים.</div>
</div>
</div>
</div>

---

## איך זה עובד? צינור ששת השלבים של המערכת

פרויקט העריכה מבוסס על שרשרת של סקילים ייעודיים (Skills) בתוך Claude Code, כאשר כל סקיל אחראי על משימה מקצועית מוגדרת:

![צינור ששת השלבים לעריכת וידאו אוטומטית מבוססת Claude Code ו-Remotion](/images/posts/claude-video-pipeline-workflow.jpg)

<div class="grid grid-cols-1 md:grid-cols-2 gap-4 my-6">
<div class="p-5 rounded-xl border border-border bg-card shadow-sm">
<div class="flex items-center gap-2 mb-2">
<span class="w-7 h-7 rounded-lg bg-blue-500/20 text-blue-400 font-bold flex items-center justify-center text-xs">1</span>
<span class="font-bold text-sm text-foreground">clean-cut (חיתוך אוטומטי)</span>
</div>
<p class="text-xs text-muted-foreground leading-relaxed">תמלול מהיר ב-AssemblyAI עם חותמות זמן מדויקות. זיהוי שתיקות, מילות היסוס וטייקים כפולים, וחיתוך Master נקי עם FFmpeg.</p>
</div>

<div class="p-5 rounded-xl border border-border bg-card shadow-sm">
<div class="flex items-center gap-2 mb-2">
<span class="w-7 h-7 rounded-lg bg-purple-500/20 text-purple-400 font-bold flex items-center justify-center text-xs">2</span>
<span class="font-bold text-sm text-foreground">make-tsx (אנימציות Remotion)</span>
</div>
<p class="text-xs text-muted-foreground leading-relaxed">זיהוי נקודות מפתח בתמליל ויצירת קומפוננטות React שמייצרות דיאגרמות, כותרות מונפשות וכרטיסיות מידע דינמיות על המסך.</p>
</div>

<div class="p-5 rounded-xl border border-border bg-card shadow-sm">
<div class="flex items-center gap-2 mb-2">
<span class="w-7 h-7 rounded-lg bg-cyan-500/20 text-cyan-400 font-bold flex items-center justify-center text-xs">3</span>
<span class="font-bold text-sm text-foreground">fake-screencast (הדמיות מסך)</span>
</div>
<p class="text-xs text-muted-foreground leading-relaxed">במקום לצלם את המסך בשידור חי, הסקיל הופך צילומי מסך בודדים להדגמות מונפשות עם תנועות עכבר חלוקות ולחיצות מדויקות.</p>
</div>

<div class="p-5 rounded-xl border border-border bg-card shadow-sm">
<div class="flex items-center gap-2 mb-2">
<span class="w-7 h-7 rounded-lg bg-emerald-500/20 text-emerald-400 font-bold flex items-center justify-center text-xs">4</span>
<span class="font-bold text-sm text-foreground">clean-audio (בידוד קול וסאונד)</span>
</div>
<p class="text-xs text-muted-foreground leading-relaxed">ניקוי רעשי רקע, הדהוד חדר ואיזון עוצמת השמע (תמיכה במנוע מקומי חינמי RNNoise או ב-ElevenLabs למקרים קשים).</p>
</div>

<div class="p-5 rounded-xl border border-border bg-card shadow-sm">
<div class="flex items-center gap-2 mb-2">
<span class="w-7 h-7 rounded-lg bg-amber-500/20 text-amber-400 font-bold flex items-center justify-center text-xs">5</span>
<span class="font-bold text-sm text-foreground">suggest-sfx (אפקטים קוליים)</span>
</div>
<p class="text-xs text-muted-foreground leading-relaxed">הלבשת צלילי מעבר, קליקים והדגשות קוליות בדיוק של מילי-שניות על הרגעים שבהם מופיעים האלמנטים הוויזואליים.</p>
</div>

<div class="p-5 rounded-xl border border-border bg-card shadow-sm">
<div class="flex items-center gap-2 mb-2">
<span class="w-7 h-7 rounded-lg bg-rose-500/20 text-rose-400 font-bold flex items-center justify-center text-xs">6</span>
<span class="font-bold text-sm text-foreground">packaging (אריזה ליוטיוב)</span>
</div>
<p class="text-xs text-muted-foreground leading-relaxed">ניסוח כותרת אופטימלית לקליקים, תיאור מלא עם חותמות זמן (Chapters) ו-3 רעיונות לתמונות ממוזערות (Thumbnails).</p>
</div>
</div>

---

## הכלים שצריך להתקין מראש

<div class="overflow-x-auto my-6 rounded-xl border border-border bg-card shadow-sm">
<table class="w-full text-sm text-right border-collapse">
<thead>
<tr class="border-b border-border bg-muted/50 text-foreground font-semibold">
<th class="p-3.5">כלי</th>
<th class="p-3.5">תפקיד במערכת</th>
<th class="p-3.5">עלות / רישוי</th>
</tr>
</thead>
<tbody class="divide-y divide-border/60 text-muted-foreground text-xs">
<tr>
<td class="p-3.5 font-bold text-foreground">VS Code</td>
<td class="p-3.5">סביבת הפיתוח והטרמינל המרכזית</td>
<td class="p-3.5 text-emerald-500 font-semibold">חינם (Microsoft)</td>
</tr>
<tr>
<td class="p-3.5 font-bold text-foreground">Claude Code</td>
<td class="p-3.5">עוזר ה-AI שמנהל ומפעיל את כל הסקילים</td>
<td class="p-3.5">מנוי Claude Pro קיים</td>
</tr>
<tr>
<td class="p-3.5 font-bold text-foreground">Python 3.10+</td>
<td class="p-3.5">הרצת סקריפטי התמלול, החיתוך ועיבוד הסאונד</td>
<td class="p-3.5 text-emerald-500 font-semibold">קוד פתוח (חינם)</td>
</tr>
<tr>
<td class="p-3.5 font-bold text-foreground">Node.js 18+</td>
<td class="p-3.5">הרצת מנוע האנימציות Remotion וקומפוננטות React</td>
<td class="p-3.5 text-emerald-500 font-semibold">קוד פתוח (חינם)</td>
</tr>
<tr>
<td class="p-3.5 font-bold text-foreground">FFmpeg</td>
<td class="p-3.5">חיתוך, קידוד וחיבור קובצי וידאו ואודיו בדיסק</td>
<td class="p-3.5 text-emerald-500 font-semibold">קוד פתוח (חינם)</td>
</tr>
</tbody>
</table>
</div>

---

## שלב אחר שלב: מהתקנה ועד לסרטון מושלם

<div class="space-y-4 my-6">

<div class="p-5 rounded-xl border border-border bg-card shadow-sm">
<div class="flex items-center gap-2.5 mb-3">
<span class="w-7 h-7 rounded-full bg-accent text-white flex items-center justify-center text-xs font-bold">1</span>
<span class="font-bold text-sm text-foreground">שכפול הפרויקט והתקנת הסביבה</span>
</div>
<p class="text-xs text-muted-foreground mb-2">פתחו את הטרמינל בתיקיית הפרויקטים והורידו את הקוד:</p>
<pre class="bg-zinc-900 border border-zinc-800 text-zinc-100 p-3.5 rounded-xl text-xs font-mono overflow-x-auto shadow-inner">git clone https://github.com/hassancs91/claude-youtube-editor
cd claude-youtube-editor</pre>
<p class="text-xs text-muted-foreground my-2">צרו סביבה וירטואלית ב-Python והתקינו את תלויות Remotion:</p>
<pre class="bg-zinc-900 border border-zinc-800 text-zinc-100 p-3.5 rounded-xl text-xs font-mono overflow-x-auto shadow-inner">python -m venv venv
venv\Scripts\python -m pip install -r requirements.txt
cd remotion && npm install && npm run gen && cd ..</pre>
</div>

<div class="p-5 rounded-xl border border-border bg-card shadow-sm">
<div class="flex items-center gap-2.5 mb-3">
<span class="w-7 h-7 rounded-full bg-accent text-white flex items-center justify-center text-xs font-bold">2</span>
<span class="font-bold text-sm text-foreground">הגדרת מפתחות ה-API בקובץ .env</span>
</div>
<p class="text-xs text-muted-foreground mb-2">שכפלו את קובץ הדוגמה והזינו מפתח של <strong>AssemblyAI</strong> (יש מסלול חינמי נדיב):</p>
<pre class="bg-zinc-900 border border-zinc-800 text-zinc-100 p-3.5 rounded-xl text-xs font-mono overflow-x-auto shadow-inner">cp .env.example .env</pre>
<pre class="bg-zinc-900 border border-zinc-800 text-zinc-100 p-3.5 rounded-xl text-xs font-mono overflow-x-auto shadow-inner">ASSEMBLYAI_API_KEY=your_assemblyai_key_here
ELEVENLABS_API_KEY=optional_key_here
GEMINI_API_KEY=optional_key_here</pre>
</div>

<div class="p-5 rounded-xl border border-border bg-card shadow-sm">
<div class="flex items-center gap-2.5 mb-3">
<span class="w-7 h-7 rounded-full bg-accent text-white flex items-center justify-center text-xs font-bold">3</span>
<span class="font-bold text-sm text-foreground">הזנת קובץ הווידאו הגולמי</span>
</div>
<p class="text-xs text-muted-foreground">הניחו את ההקלטה שבה אתם מדברים אל המצלמה בתיקייה:</p>
<pre class="bg-zinc-900 border border-zinc-800 text-zinc-100 p-3.5 rounded-xl text-xs font-mono overflow-x-auto shadow-inner">videos/video-1/recording.mp4</pre>
</div>

<div class="p-5 rounded-xl border border-border bg-card shadow-sm">
<div class="flex items-center gap-2.5 mb-3">
<span class="w-7 h-7 rounded-full bg-emerald-500 text-white flex items-center justify-center text-xs font-bold">4</span>
<span class="font-bold text-sm text-foreground">הרצת שרשרת העריכה ב-Claude Code</span>
</div>
<p class="text-xs text-muted-foreground mb-2">הפעילו את Claude Code והריצו את הפקודות בזה אחר זה (פקודות טרמינל ישירות):</p>
<div class="space-y-2.5 text-xs">
<div class="p-3 rounded-xl bg-zinc-900 border border-zinc-800 flex items-center justify-between font-mono">
<span class="text-emerald-400 font-bold tracking-wide">clean cut videos/video-1</span>
<span class="text-zinc-300 font-sans text-xs">חיתוך שתיקות וטעויות</span>
</div>
<div class="p-3 rounded-xl bg-zinc-900 border border-zinc-800 flex items-center justify-between font-mono">
<span class="text-cyan-400 font-bold tracking-wide">add TSX beats to video-1</span>
<span class="text-zinc-300 font-sans text-xs">רינדור אנימציות Remotion</span>
</div>
<div class="p-3 rounded-xl bg-zinc-900 border border-zinc-800 flex items-center justify-between font-mono">
<span class="text-amber-400 font-bold tracking-wide">clean the audio for video-1</span>
<span class="text-zinc-300 font-sans text-xs">בידוד קול ואיזון שמע</span>
</div>
<div class="p-3 rounded-xl bg-zinc-900 border border-zinc-800 flex items-center justify-between font-mono">
<span class="text-purple-400 font-bold tracking-wide">suggest sfx for video-1</span>
<span class="text-zinc-300 font-sans text-xs">אפקטים קוליים מתוזמנים</span>
</div>
</div>
</div>

</div>

---

## שקיפות עלויות: כמה זה באמת עולה?

<div class="grid grid-cols-1 md:grid-cols-3 gap-4 my-6">
<div class="p-5 rounded-xl border border-border bg-card text-center">
<div class="text-xs text-muted-foreground mb-1">פרויקט וספריות קוד</div>
<div class="text-lg font-bold text-emerald-500 mb-1">0$ (חינם)</div>
<div class="text-[11px] text-muted-foreground">רישיון קוד פתוח MIT מלא</div>
</div>

<div class="p-5 rounded-xl border border-border bg-card text-center">
<div class="text-xs text-muted-foreground mb-1">חיתוך וסאונד בסיסי</div>
<div class="text-lg font-bold text-emerald-500 mb-1">0$ לניסיון</div>
<div class="text-[11px] text-muted-foreground">מסלול חינם ב-AssemblyAI + RNNoise מקומי</div>
</div>

<div class="p-5 rounded-xl border border-border bg-card text-center">
<div class="text-xs text-muted-foreground mb-1">ניהול AI בטרמינל</div>
<div class="text-lg font-bold text-accent mb-1">~20$/חודש</div>
<div class="text-[11px] text-muted-foreground">מנוי Claude Pro הרגיל שמשמש לפיתוח</div>
</div>
</div>

---

## למי מתאים הפתרון ולמה הוא ישנה לכם את העבודה?

<div class="grid grid-cols-1 md:grid-cols-2 gap-6 my-6">
<div class="p-6 rounded-2xl border border-border bg-card">
<div class="font-bold text-base text-foreground mb-3">👥 למי זה מתאים?</div>
<ul class="text-xs text-muted-foreground space-y-2.5 leading-relaxed">
<li>• <strong>יוצרי תוכן וערוצי הדרכה:</strong> המעוניינים להפיק סרטונים מקצועיים ללא עורכים חיצוניים.</li>
<li>• <strong>יזמים ומפתחים עצמאיים:</strong> שרוצים להציג את המוצרים שלהם מבלי לבזבז ימים שלמים על עריכה.</li>
<li>• <strong>אנשי שיווק ואוטומציה:</strong> המעוניינים להפוך חומרי גלם לנכסים דיגיטליים מעוצבים כחלק מצינור תוכן.</li>
</ul>
</div>

<div class="p-6 rounded-2xl border border-border bg-card">
<div class="font-bold text-base text-foreground mb-3">💡 היתרונות המרכזיים</div>
<ul class="text-xs text-muted-foreground space-y-2.5 leading-relaxed">
<li>• <strong class="text-emerald-500">חיסכון של 80% מזמן ההפקה:</strong> השקעה רק בהקלטה ואישור קצר.</li>
<li>• <strong class="text-accent">עקביות מותגית:</strong> כל האנימציות נוצרות מקוד React השומר על העיצוב שלכם.</li>
<li>• <strong class="text-foreground">הקלטה ללא לחץ:</strong> הידיעה שטעויות דיבור נחתכות אוטומטית מאפשרת לדבר בחופשיות.</li>
</ul>
</div>
</div>

---

<div class="rounded-2xl border border-accent/30 bg-gradient-to-r from-accent/15 via-accent/5 to-transparent p-6 my-8 shadow-sm">
<div class="font-bold text-base text-foreground mb-2">🚀 סיכום</div>
<p class="text-xs text-muted-foreground leading-relaxed">
שילוב של כלי שורת פקודה כמו FFmpeg, ספריות גרפיקה כמו Remotion וסוכני AI כמו Claude Code מסמן נקודת מפנה בעולם יצירת התוכן. במקום להילחם בתוכנות עריכה מיושנות או להוציא אלפי שקלים על עורכים חיצוניים, אתם יכולים כעת לנהל אולפן הפקה שלם ישירות מהטרמינל שלכם.
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

<a href="/posts/2026-09-21-free-ai-images-claude-code-cloudflare" class="group flex flex-col overflow-hidden rounded-2xl border border-border/80 bg-card transition-all duration-300 hover:-translate-y-1 hover:border-accent/60 hover:shadow-lg no-underline">
<div class="aspect-video w-full overflow-hidden bg-muted">
<img src="/images/posts/free-ai-images-claude-code-cloudflare.jpg" alt="ייצור תמונות חינם עם Cloudflare" class="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105 m-0 border-0" />
</div>
<div class="flex flex-1 flex-col p-4">
<span class="text-xs font-bold text-accent mb-1">מדריך חיסכון בעלויות</span>
<h4 class="text-base font-bold text-foreground group-hover:text-accent transition-colors m-0 leading-snug">איך לייצר תמונות AI בחינם ישירות מ-Claude Code עם Cloudflare</h4>
<p class="text-xs text-muted-foreground mt-2 line-clamp-2 leading-relaxed">הפקת כ-170 תמונות ביום במודל FLUX.1 schnell באפס עלות וללא צורך במעבד גרפי.</p>
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
