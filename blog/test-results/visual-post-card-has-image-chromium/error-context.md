# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: visual.spec.ts >> post card has image
- Location: tests\visual.spec.ts:22:1

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: locator('li').first().locator('img, .bg-gradient-to-br').first()
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" with timeout 5000ms
  - waiting for locator('li').first().locator('img, .bg-gradient-to-br').first()

```

# Page snapshot

```yaml
- generic [active] [ref=e1]:
  - link "דלג לתוכן" [ref=e2] [cursor=pointer]:
    - /url: "#main-content"
  - banner [ref=e3]:
    - generic [ref=e4]:
      - link "עולם ה AI" [ref=e5] [cursor=pointer]:
        - /url: /
      - navigation [ref=e6]:
        - list [ref=e7]:
          - listitem [ref=e8]:
            - link "פוסטים" [ref=e9] [cursor=pointer]:
              - /url: /posts
          - listitem [ref=e10]:
            - link "תגיות" [ref=e11] [cursor=pointer]:
              - /url: /tags
          - listitem [ref=e12]:
            - link "אודות" [ref=e13] [cursor=pointer]:
              - /url: /about
          - listitem [ref=e14]:
            - link "ארכיון" [ref=e15] [cursor=pointer]:
              - /url: /archives
              - img [ref=e16]
              - generic [ref=e20]: ארכיון
          - listitem [ref=e21]:
            - link "חיפוש" [ref=e22] [cursor=pointer]:
              - /url: /search
              - img [ref=e23]
              - generic [ref=e27]: חיפוש
          - listitem [ref=e28]:
            - button "light" [ref=e29] [cursor=pointer]:
              - img [ref=e30]
              - img
  - main [ref=e33]:
    - generic [ref=e34]:
      - img [ref=e35]
      - generic [ref=e37]:
        - generic [ref=e38]:
          - heading "עולם ה AI" [level=1] [ref=e39]
          - link "rss feed" [ref=e40] [cursor=pointer]:
            - /url: /rss.xml
            - img [ref=e41]
            - generic [ref=e46]: RSS Feed
        - paragraph [ref=e47]: בלוג בעברית על כלי AI חדשים, מדריכים נגישים והסברים ישירים — למי שרוצה להבין איך להשתמש באמת ב-AI, בלי בלה-בלה שיווקי. פוסטים חדשים מדי שבוע.
        - generic [ref=e48]:
          - generic [ref=e49]: "קישורים:"
          - generic [ref=e50]:
            - link "עולם ה AI on GitHub" [ref=e51] [cursor=pointer]:
              - /url: https://github.com/satnaing/astro-paper
              - img [ref=e52]
              - generic [ref=e55]: עולם ה AI on GitHub
            - link "עולם ה AI on X" [ref=e56] [cursor=pointer]:
              - /url: https://x.com/username
              - img [ref=e57]
              - generic [ref=e61]: עולם ה AI on X
            - link "עולם ה AI on LinkedIn" [ref=e62] [cursor=pointer]:
              - /url: https://www.linkedin.com/in/username/
              - img [ref=e63]
              - generic [ref=e67]: עולם ה AI on LinkedIn
            - link "Send an email to עולם ה AI" [ref=e68] [cursor=pointer]:
              - /url: mailto:yourmail@gmail.com
              - img [ref=e69]
              - generic [ref=e73]: Send an email to עולם ה AI
    - generic [ref=e74]:
      - heading "מומלצים" [level=2] [ref=e75]
      - list [ref=e76]:
        - listitem [ref=e77]:
          - link "🤖 ברוכים הבאים לעולם ה AI 6 Apr, 2026 בלוג חדש בעברית על כלי AI, מדריכים נגישים, והסברים ישירים — למי שרוצה להבין איך להשתמש באמת ב-AI." [ref=e78] [cursor=pointer]:
            - /url: /posts/welcome
            - generic [ref=e81]: 🤖
            - generic [ref=e82]:
              - heading "ברוכים הבאים לעולם ה AI" [level=3] [ref=e83]
              - generic [ref=e84]:
                - img [ref=e85]
                - time [ref=e88]: 6 Apr, 2026
              - paragraph [ref=e89]: בלוג חדש בעברית על כלי AI, מדריכים נגישים, והסברים ישירים — למי שרוצה להבין איך להשתמש באמת ב-AI.
    - generic [ref=e90]:
      - heading "פוסטים אחרונים" [level=2] [ref=e91]
      - list [ref=e92]:
        - listitem [ref=e93]:
          - 'link "🤖 8 כלי אוטומציה עם AI שיכולים לחסוך לכם שעות של עבודה חוזרת כל שבוע 6 Apr, 2026 כל מי שעובד מול מחשב מכיר את התחושה הזו: חצי מהיום עובר על דברים שאפשר היה לעשות אוטומטית. העברת מידע מטופס לטבלה, שליחת מייל מעקב אחרי פגישה, עדכון מערכת ניהול" [ref=e94] [cursor=pointer]':
            - /url: /posts/2026-04-06-ai-automation-tools
            - generic [ref=e97]: 🤖
            - generic [ref=e98]:
              - heading "8 כלי אוטומציה עם AI שיכולים לחסוך לכם שעות של עבודה חוזרת כל שבוע" [level=3] [ref=e99]
              - generic [ref=e100]:
                - img [ref=e101]
                - time [ref=e104]: 6 Apr, 2026
              - paragraph [ref=e105]: "כל מי שעובד מול מחשב מכיר את התחושה הזו: חצי מהיום עובר על דברים שאפשר היה לעשות אוטומטית. העברת מידע מטופס לטבלה, שליחת מייל מעקב אחרי פגישה, עדכון מערכת ניהול"
        - listitem [ref=e106]:
          - link "🤖 Perplexity — מנוע החיפוש שבאמת עונה לך על השאלה 6 Apr, 2026 מנוע חיפוש AI שמסכם תשובות עם מקורות — חוסך את שלב הסינון ומאפשר שיחה עם המידע במקום חיפוש רגיל" [ref=e107] [cursor=pointer]:
            - /url: /posts/2026-04-06-perplexity-mnv-hhyfvs-sv-mt-vnh-lkh-l-hs-lh
            - generic [ref=e110]: 🤖
            - generic [ref=e111]:
              - heading "Perplexity — מנוע החיפוש שבאמת עונה לך על השאלה" [level=3] [ref=e112]
              - generic [ref=e113]:
                - img [ref=e114]
                - time [ref=e117]: 6 Apr, 2026
              - paragraph [ref=e118]: מנוע חיפוש AI שמסכם תשובות עם מקורות — חוסך את שלב הסינון ומאפשר שיחה עם המידע במקום חיפוש רגיל
    - link "כל הפוסטים" [ref=e120] [cursor=pointer]:
      - /url: /posts/
      - text: כל הפוסטים
      - img [ref=e121]
  - contentinfo [ref=e125]:
    - generic [ref=e126]:
      - generic [ref=e127]:
        - link "עולם ה AI on GitHub" [ref=e128] [cursor=pointer]:
          - /url: https://github.com/satnaing/astro-paper
          - img [ref=e129]
          - generic [ref=e132]: עולם ה AI on GitHub
        - link "עולם ה AI on X" [ref=e133] [cursor=pointer]:
          - /url: https://x.com/username
          - img [ref=e134]
          - generic [ref=e138]: עולם ה AI on X
        - link "עולם ה AI on LinkedIn" [ref=e139] [cursor=pointer]:
          - /url: https://www.linkedin.com/in/username/
          - img [ref=e140]
          - generic [ref=e144]: עולם ה AI on LinkedIn
        - link "Send an email to עולם ה AI" [ref=e145] [cursor=pointer]:
          - /url: mailto:yourmail@gmail.com
          - img [ref=e146]
          - generic [ref=e150]: Send an email to עולם ה AI
      - generic [ref=e151]:
        - generic [ref=e152]: © 2026
        - generic [ref=e153]: "|"
        - generic [ref=e154]: כל הזכויות שמורות.
```

# Test source

```ts
  1  | import { test, expect } from "@playwright/test";
  2  | import { fileURLToPath } from "url";
  3  | import path from "path";
  4  | 
  5  | const SS = path.join(path.dirname(fileURLToPath(import.meta.url)), "screenshots");
  6  | 
  7  | test("homepage looks correct", async ({ page }) => {
  8  |   await page.goto("/");
  9  |   await page.waitForLoadState("networkidle");
  10 | 
  11 |   // Hero image loaded
  12 |   const heroImg = page.locator("#hero img").first();
  13 |   await expect(heroImg).toBeVisible();
  14 | 
  15 |   // Post cards exist
  16 |   const cards = page.locator("li a.group");
  17 |   await expect(cards.first()).toBeVisible();
  18 | 
  19 |   await page.screenshot({ path: `${SS}/homepage.png`, fullPage: true });
  20 | });
  21 | 
  22 | test("post card has image", async ({ page }) => {
  23 |   await page.goto("/");
  24 |   await page.waitForLoadState("networkidle");
  25 | 
  26 |   // Each card should have an img or the gradient fallback
  27 |   const firstCard = page.locator("li").first();
  28 |   const cardImage = firstCard.locator("img, .bg-gradient-to-br");
> 29 |   await expect(cardImage.first()).toBeVisible();
     |                                   ^ Error: expect(locator).toBeVisible() failed
  30 | 
  31 |   await page.screenshot({ path: `${SS}/card-image.png` });
  32 | });
  33 | 
  34 | test("post page has hero image", async ({ page }) => {
  35 |   await page.goto("/");
  36 |   // Click first post
  37 |   const firstLink = page.locator("li a.group").first();
  38 |   await firstLink.click();
  39 |   await page.waitForLoadState("networkidle");
  40 | 
  41 |   await page.screenshot({ path: `${SS}/post-page.png`, fullPage: true });
  42 | });
  43 | 
  44 | test("dark mode looks correct", async ({ page }) => {
  45 |   await page.goto("/");
  46 |   // Toggle dark mode
  47 |   await page.click('[aria-label="light theme"], [aria-label="dark theme"], button[title*="theme"], #theme-btn');
  48 |   await page.waitForTimeout(300);
  49 |   await page.screenshot({ path: `${SS}/homepage-dark.png`, fullPage: true });
  50 | });
  51 | 
```