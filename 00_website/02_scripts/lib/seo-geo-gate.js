import "dotenv/config";

/**
 * Jev Rapid Pre-Publish SEO & GEO Quality Gate.
 * Validates Hebrew natural fluency, actionable meta descriptions, and Zero-Click Answer blocks (<300ms).
 */

const VERCEL_AI_GATEWAY_URL = "https://gateway.ai.vercel.com/v1/chat/completions";
const JEV_MODEL = process.env.AI_MODEL || "typesafe-ai/jev";

/**
 * Evaluates blog post content and metadata against SEO and Generative Engine Optimization (GEO) standards.
 */
export async function evaluateSeoGeoQuality({ title, metaDescription, content, tags = [] }) {
  const apiKey = process.env.AI_GATEWAY_API_KEY;

  const payload = {
    title: title || "",
    metaDescription: metaDescription || "",
    contentSample: content ? content.slice(0, 2000) : "",
    tags,
  };

  if (!apiKey) {
    return getFallbackSeoGeoEvaluation(payload);
  }

  const systemInstruction = `You are Jev, a rapid Pre-Publish SEO & Generative Engine Optimization (GEO) Quality Gate for "עולם ה-AI" (AI World Blog, Israel).
Your goal is to ensure every article ranks in Google Search and is cited by AI Search Engines (Perplexity, SearchGPT, Google AI Overviews).

Evaluate the following criteria:
1. hebrewGrammarNatural (boolean): Is the Hebrew natural, authoritative, and free of clunky machine-translation artifacts?
2. metaDescriptionActionable (boolean): Is the meta description 100-165 chars, compelling, and actionable?
3. containsClearAnswerBlock (boolean): Does the post start with or contain a concise 40-70 word zero-click answer / clear definition suitable for direct LLM citation?
4. missingKeywords (array of strings): Critical SEO/GEO search terms missing from the intro/headings.
5. score (integer 1-10): Overall SEO/GEO score.
6. passesQualityBar (boolean): True if score >= 7 AND hebrewGrammarNatural AND metaDescriptionActionable AND containsClearAnswerBlock.
7. feedback (string in Hebrew): 1-2 constructive sentences on how to improve.

Respond STRICTLY with valid JSON:
{
  "hebrewGrammarNatural": boolean,
  "metaDescriptionActionable": boolean,
  "containsClearAnswerBlock": boolean,
  "missingKeywords": string[],
  "score": number,
  "passesQualityBar": boolean,
  "feedback": string
}`;

  try {
    const startTime = Date.now();
    const response = await fetch(VERCEL_AI_GATEWAY_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        model: JEV_MODEL,
        temperature: 0,
        messages: [
          { role: "system", content: systemInstruction },
          { role: "user", content: `Evaluate this post for pre-publish SEO/GEO gate:\n${JSON.stringify(payload)}` },
        ],
        response_format: { type: "json_object" },
      }),
    });

    if (!response.ok) {
      return getFallbackSeoGeoEvaluation(payload);
    }

    const data = await response.json();
    const durationMs = Date.now() - startTime;
    const rawContent = data.choices?.[0]?.message?.content;

    let parsed = {};
    try {
      parsed = JSON.parse(rawContent);
    } catch {
      return getFallbackSeoGeoEvaluation(payload);
    }

    const score = typeof parsed.score === "number" ? parsed.score : 7;
    const hebrewGrammarNatural = parsed.hebrewGrammarNatural !== false;
    const metaDescriptionActionable = parsed.metaDescriptionActionable !== false;
    const containsClearAnswerBlock = parsed.containsClearAnswerBlock !== false;
    const passesQualityBar =
      Boolean(parsed.passesQualityBar) && score >= 7 && hebrewGrammarNatural && containsClearAnswerBlock;

    return {
      hebrewGrammarNatural,
      metaDescriptionActionable,
      containsClearAnswerBlock,
      missingKeywords: Array.isArray(parsed.missingKeywords) ? parsed.missingKeywords : [],
      score,
      passesQualityBar,
      feedback: parsed.feedback || "עומד ברף האיכות של SEO ו-GEO",
      durationMs,
    };
  } catch (e) {
    return getFallbackSeoGeoEvaluation(payload);
  }
}

/**
 * Heuristic fallback evaluation if AI gateway is unreachable (0ms).
 */
export function getFallbackSeoGeoEvaluation({ title = "", metaDescription = "", content = "", contentSample = "" }) {
  const fullText = content || contentSample || "";
  const metaLen = (metaDescription || "").trim().length;
  const metaDescriptionActionable = metaLen >= 40 && metaLen <= 220;

  // Check for clear answer block or callout block in the top 1500 chars
  const intro = fullText.slice(0, 1500);
  const containsClearAnswerBlock =
    intro.includes(">") ||
    intro.includes("תקציר") ||
    intro.includes("בשורה אחת") ||
    intro.includes("הסבר קצר") ||
    intro.includes("## מה זה") ||
    intro.includes("## מהו");

  // Check for unnatural phrases
  const hasUnnaturalPatterns =
    intro.includes("בתור מודל שפה") ||
    intro.includes("כמודל שפה") ||
    intro.includes("חשוב לזכור כי המידע") ||
    fullText.length < 200;

  const hebrewGrammarNatural = !hasUnnaturalPatterns;
  const score = (metaDescriptionActionable ? 3 : 1) + (containsClearAnswerBlock ? 4 : 2) + (hebrewGrammarNatural ? 3 : 1);
  const passesQualityBar = score >= 7 && metaDescriptionActionable && containsClearAnswerBlock && hebrewGrammarNatural;

  const missingKeywords = [];
  if (!intro.includes("AI") && !intro.includes("בינה מלאכותית")) {
    missingKeywords.push("בינה מלאכותית");
  }

  let feedback = "המאמר עומד ברף האיכות.";
  if (!passesQualityBar) {
    feedback = `נדרש תיקון: ${!metaDescriptionActionable ? "תיאור מטא קצר או חסר. " : ""}${!containsClearAnswerBlock ? "חסרה פסקת תשובה ישירה (Zero-Click Answer Block) בתחילת הפוסט. " : ""}`;
  }

  return {
    hebrewGrammarNatural,
    metaDescriptionActionable,
    containsClearAnswerBlock,
    missingKeywords,
    score,
    passesQualityBar,
    feedback,
    durationMs: 0,
  };
}
