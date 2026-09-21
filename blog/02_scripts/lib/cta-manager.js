/**
 * Dynamic Monetization CTA Manager (Phase 3).
 * Injects high-converting Hebrew CTAs based on Jev evaluation and commercial intent.
 */

export const CTA_TEMPLATES = {
  course: {
    title: "🎓 רוצים לשלוט בכלי AI מעשיים בעסק שלכם?",
    body: "הצטרפו לתכנית ההכשרה המעשית שלנו לבינה מלאכותית — עם דוגמאות חיות, תבניות עבודה מוכנות וליווי מקצועי.",
    buttonText: "לפרטים והרשמה לקורס המלא ←",
    buttonUrl: "https://google-ai-pro-drab.vercel.app/",
  },
  consulting: {
    title: "💼 צריכים ליווי והטמעת AI בארגון או בעסק?",
    body: "משרד רואה חשבון רונן עמוס מתמחה באוטומציה עסקית, ביקורת מערכות AI והטמעת סוכנים חכמים לחיסכון של עשרות שעות עבודה בחודש.",
    buttonText: "לתיאום שיחת ייעוץ אסטרטגית ←",
    buttonUrl: "https://ronenamoscpa.co.il",
  },
  tools: {
    title: "🛠️ ארגז הכלים המלא למפתחים ויוצרים",
    body: "קבלו גישה למאגר הפרומפטים, הסקריפטים וסוכני ה-AI המובילים שאנחנו משתמשים בהם ביום-יום.",
    buttonText: "לכל המדריכים וארגז הכלים ←",
    buttonUrl: "/tags/ai",
  },
  newsletter: {
    title: "📬 הישארו מעודכנים לפני כולם בעולם ה-AI",
    body: "הצטרפו למאות מקצוענים שמקבלים מדי שבוע סקירות עומק, כלים חדשים וניתוחים מעשיים ישירות למייל.",
    buttonText: "להרשמה לניוזלטר השבועי ←",
    buttonUrl: "#newsletter",
  },
};

/**
 * Builds a styled Hebrew CTA block in Markdown format.
 */
export function buildCtaBlock(ctaType = "course") {
  const cta = CTA_TEMPLATES[ctaType] || CTA_TEMPLATES.course;

  return `\n\n---

> ### ${cta.title}
> ${cta.body}
> 
> **[${cta.buttonText}](${cta.buttonUrl})**
`;
}

/**
 * Injects the selected CTA block into post markdown content.
 */
export function injectDynamicCta(content, jevEval) {
  if (!content) return "";
  const ctaType = jevEval?.recommendedCta || "course";
  const ctaBlock = buildCtaBlock(ctaType);
  return content.trim() + ctaBlock;
}
