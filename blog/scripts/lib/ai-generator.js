import { generateObject, generateText } from "ai";
import { createAnthropic } from "@ai-sdk/anthropic";
import { z } from "zod";
import { STYLE_REFERENCE, STYLE_EXAMPLES } from "./style-examples.js";

const anthropic = createAnthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
const model = anthropic("claude-sonnet-4-5");

const postSchema = z.object({
  title: z.string().describe("SEO-optimized Hebrew title, 40-70 chars"),
  description: z.string().describe("Meta description in Hebrew, 120-160 chars"),
  slug: z.string().describe("URL slug in English, lowercase, hyphenated"),
  altText: z.string().describe("Image alt text in Hebrew, 50-100 chars"),
  tags: z.array(z.string()).describe("3-5 topic tags in Hebrew or English"),
  content: z.string().describe("Full post body in Hebrew markdown, 1000-1500 words"),
});

function buildPrompt({ name, prompt, urlSource, partialContent, scrapedContent }) {
  const sources = [];

  if (prompt) sources.push(`נושא/פרומפט: ${prompt}`);
  if (name) sources.push(`שם/כותרת ראשונית: ${name}`);
  if (urlSource) sources.push(`URL מקור לעיון: ${urlSource}`);
  if (scrapedContent)
    sources.push(
      `תוכן שחולץ מה-URL (להשראה בלבד, אל תעתיק - כתב מחדש בקול שלך):\n${scrapedContent.slice(0, 4000)}`
    );
  if (partialContent) sources.push(`תוכן חלקי שצריך להשלים:\n${partialContent}`);

  return `${STYLE_REFERENCE}

${STYLE_EXAMPLES}

---

משימה: כתב פוסט מלא לבלוג בעברית בהתבסס על המקורות הבאים:

${sources.join("\n\n")}

הנחיות:
- אורך: 1000-1500 מילים
- שפה: עברית בלבד (חוץ משמות כלים באנגלית)
- פורמט: Markdown
- אם יש URL מקור - קח השראה אבל כתב לגמרי מחדש, אל תעתיק
- אל תחזור על הכותרת בתוך ה-content (היא נפרדת)
- ה-slug צריך להיות באנגלית בלבד, אותיות קטנות, עם מקפים`;
}

export async function generatePost({
  name,
  prompt,
  urlSource,
  partialContent,
  scrapedContent,
}) {
  const userPrompt = buildPrompt({ name, prompt, urlSource, partialContent, scrapedContent });

  const result = await generateObject({
    model,
    schema: postSchema,
    prompt: userPrompt,
    maxOutputTokens: 8000,
  });

  const wordCount = result.object.content.split(/\s+/).filter(Boolean).length;

  return {
    ...result.object,
    wordCount,
  };
}
