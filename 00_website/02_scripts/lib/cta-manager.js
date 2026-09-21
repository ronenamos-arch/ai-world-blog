/**
 * Dynamic Monetization CTA Manager.
 * Injects high-converting Hebrew CTAs based on Jev evaluation, audience persona, and commercial intent.
 */

export const CTA_TEMPLATES = {
  consulting: {
    id: "consulting",
    title: "💼 צריכים ליווי והטמעת AI בארגון או בעסק?",
    body: "משרד רואה חשבון רונן עמוס מתמחה באוטומציה עסקית, ביקורת מערכות AI והטמעת סוכנים חכמים לחיסכון של עשרות שעות עבודה בחודש.",
    buttonText: "לתיאום שיחת ייעוץ אסטרטגית וביקורת AI ←",
    buttonUrl: "https://ronenamoscpa.co.il",
    badge: "ייעוץ וביקורת לחברות ועסקים",
  },
  course: {
    id: "course",
    title: "🎓 רוצים לשלוט בכלי AI מעשיים בעסק שלכם?",
    body: "הצטרפו לתכנית ההכשרה המעשית שלנו לבינה מלאכותית — עם דוגמאות חיות, תבניות עבודה מוכנות וליווי מקצועי צעד-אחר-צעד.",
    buttonText: "לפרטים והרשמה לרשימת ההמתנה לקורס המלא ←",
    buttonUrl: "https://google-ai-pro-drab.vercel.app/",
    badge: "הכשרה מעשית מקיפה",
  },
  tools: {
    id: "tools",
    title: "🛠️ ארגז הכלים המלא למפתחים ויוצרים",
    body: "קבלו גישה למאגר הפרומפטים, הסקריפטים וסוכני ה-AI המובילים שאנחנו משתמשים בהם ביום-יום לייעול תהליכי פיתוח.",
    buttonText: "לכל המדריכים וארגז הכלים הטכנולוגי ←",
    buttonUrl: "/tags/ai",
    badge: "סביבת עבודה למפתחים",
  },
  newsletter: {
    id: "newsletter",
    title: "📬 הישארו מעודכנים לפני כולם בעולם ה-AI",
    body: "הצטרפו למאות מקצוענים שמקבלים מדי שבוע סקירות עומק, כלים חדשים וניתוחים מעשיים ישירות למייל.",
    buttonText: "להרשמה לניוזלטר השבועי ←",
    buttonUrl: "#newsletter",
    badge: "עדכונים שבועיים בלעדיים",
  },
};

/**
 * Determines the most profitable and relevant CTA based on Jev evaluation.
 */
export function resolveCtaType(jevEval = {}) {
  const { recommendedCta, targetAudience, suggestedPostType, commercialIntent } = jevEval;

  if (recommendedCta && CTA_TEMPLATES[recommendedCta]) {
    return recommendedCta;
  }

  // Finance / Corporate / High Commercial Intent -> CPA & Consulting
  if (
    targetAudience === "finance" ||
    targetAudience === "business_owners" ||
    commercialIntent === "high" ||
    suggestedPostType === "use_case"
  ) {
    return "consulting";
  }

  // Beginners / Step-by-step guides -> Course & Workshops
  if (targetAudience === "beginners" || suggestedPostType === "tutorial") {
    return "course";
  }

  // Developers / Tools / Technical -> Tools & Affiliates
  if (targetAudience === "developers" || suggestedPostType === "comparison" || suggestedPostType === "tool_explainer") {
    return "tools";
  }

  return "newsletter";
}

/**
 * Builds a styled Hebrew CTA block in Markdown format.
 */
export function buildCtaBlock(ctaType = "course") {
  const resolvedKey = CTA_TEMPLATES[ctaType] ? ctaType : "course";
  const cta = CTA_TEMPLATES[resolvedKey];

  return `\n\n---

> ### ${cta.title}
> **${cta.badge}**
> 
> ${cta.body}
> 
> 👉 **[${cta.buttonText}](${cta.buttonUrl})**
`;
}

/**
 * Injects the dynamic CTA block into post markdown content.
 */
export function injectDynamicCta(content, jevEval) {
  if (!content) return "";
  const ctaType = resolveCtaType(jevEval);
  const ctaBlock = buildCtaBlock(ctaType);
  return content.trim() + ctaBlock;
}
