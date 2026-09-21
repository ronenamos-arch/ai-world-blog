import "dotenv/config";

/**
 * Jev Real-Time Lead Scoring & Qualification Module.
 * Evaluates inbound contact inquiries, classifies commercial intent, and routes VIP leads in <300ms.
 */

const VERCEL_AI_GATEWAY_URL = "https://gateway.ai.vercel.com/v1/chat/completions";
const JEV_MODEL = process.env.AI_MODEL || "typesafe-ai/jev";

export async function scoreLeadWithJev(leadPayload) {
  const apiKey = process.env.AI_GATEWAY_API_KEY;

  const {
    name = "",
    email = "",
    phone = "",
    company = "",
    message = "",
    sourceUrl = "",
    estimatedEmployees = "",
  } = leadPayload || {};

  // If no gateway API key, use instant heuristic fallback
  if (!apiKey) {
    return getFallbackLeadScore(leadPayload);
  }

  const systemInstruction = `You are Jev, a high-speed lead scoring and triage engine for "עולם ה-AI" and Ronen Amos CPA & AI Consulting.
Analyze inbound user inquiries and assign:
- score: 0-100 integer representing commercial conversion value.
- urgency: one of ["urgent", "high", "normal", "low"].
- targetService: one of ["cpa_consulting", "ai_course", "tools_affiliate", "newsletter", "spam"].
- budgetTier: one of ["enterprise", "mid_market", "smb", "individual", "unknown"].
- routeAction: one of ["whatsapp_urgent", "notion_vip", "email_queue", "discard_spam"].
- summaryReason: 1 sentence in Hebrew explaining why this score was assigned.

Guidelines:
- Enterprise / Corporate / Audits / Tax / B2B Automation -> score 80-100, targetService: "cpa_consulting", routeAction: "whatsapp_urgent".
- Individuals wanting to learn AI / prompt engineering -> score 50-75, targetService: "ai_course", routeAction: "email_queue".
- Tool integration / coding queries -> score 40-70, targetService: "tools_affiliate", routeAction: "email_queue".
- Spam / gibberish / low quality -> score 0-20, routeAction: "discard_spam".

Respond STRICTLY in JSON format matching:
{
  "score": number,
  "urgency": string,
  "targetService": string,
  "budgetTier": string,
  "routeAction": string,
  "summaryReason": string
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
          {
            role: "user",
            content: `Evaluate this lead:\n${JSON.stringify({
              name,
              email,
              phone,
              company,
              message,
              sourceUrl,
              estimatedEmployees,
            })}`,
          },
        ],
        response_format: { type: "json_object" },
      }),
    });

    if (!response.ok) {
      return getFallbackLeadScore(leadPayload);
    }

    const data = await response.json();
    const durationMs = Date.now() - startTime;
    const content = data.choices?.[0]?.message?.content;

    let parsed = {};
    try {
      parsed = JSON.parse(content);
    } catch {
      return getFallbackLeadScore(leadPayload);
    }

    return {
      score: typeof parsed.score === "number" ? parsed.score : 60,
      urgency: parsed.urgency || "normal",
      targetService: parsed.targetService || "cpa_consulting",
      budgetTier: parsed.budgetTier || "smb",
      routeAction: parsed.routeAction || "notion_vip",
      summaryReason: parsed.summaryReason || "ניתוח ליד הושלם בהצלחה",
      isVip: (parsed.score || 0) >= 80,
      durationMs,
    };
  } catch (err) {
    return getFallbackLeadScore(leadPayload);
  }
}

/**
 * Intelligent instant heuristic fallback for lead scoring (0ms).
 */
export function getFallbackLeadScore(lead) {
  const text = `${lead.company || ""} ${lead.message || ""} ${lead.sourceUrl || ""}`.toLowerCase();

  // Spam detection
  if (text.includes("viagra") || text.includes("crypto casino") || text.length < 5) {
    return {
      score: 5,
      urgency: "low",
      targetService: "spam",
      budgetTier: "unknown",
      routeAction: "discard_spam",
      summaryReason: "זוהה כספאם או פנייה ריקה",
      isVip: false,
      durationMs: 0,
    };
  }

  // High ticket CPA & Enterprise Consulting
  if (
    text.includes("חברה") ||
    text.includes("רואה חשבון") ||
    text.includes("ביקורת") ||
    text.includes("ייעוץ") ||
    text.includes("ארגון") ||
    text.includes("עובדים") ||
    text.includes("אוטומציה עסקית") ||
    text.includes("cpa") ||
    text.includes("enterprise")
  ) {
    return {
      score: 92,
      urgency: "urgent",
      targetService: "cpa_consulting",
      budgetTier: "enterprise",
      routeAction: "whatsapp_urgent",
      summaryReason: "ליד חם: התעניינות בייעוץ עסקי / ביקורת AI לארגון",
      isVip: true,
      durationMs: 0,
    };
  }

  // Course / Workshops
  if (text.includes("קורס") || text.includes("סדנא") || text.includes("ללמוד") || text.includes("course")) {
    return {
      score: 70,
      urgency: "normal",
      targetService: "ai_course",
      budgetTier: "individual",
      routeAction: "email_queue",
      summaryReason: "התעניינות בקורס או סדנת הכשרה מעשית ב-AI",
      isVip: false,
      durationMs: 0,
    };
  }

  // General inquiry
  return {
    score: 65,
    urgency: "normal",
    targetService: "cpa_consulting",
    budgetTier: "smb",
    routeAction: "notion_vip",
    summaryReason: "פנייה כללית בנושאי בינה מלאכותית",
    isVip: false,
    durationMs: 0,
  };
}
