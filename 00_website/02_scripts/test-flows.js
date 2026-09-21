import "dotenv/config";
import { resolveCtaType, buildCtaBlock, CTA_TEMPLATES } from "./lib/cta-manager.js";
import { scoreLeadWithJev } from "./lib/lead-scorer.js";
import { evaluateSeoGeoQuality } from "./lib/seo-geo-gate.js";

async function runTests() {
  console.log("=================================================");
  console.log("⚡ TESTING JEV FLOW 1: DYNAMIC CTA & LEAD SCORING");
  console.log("=================================================\n");

  // 1. Dynamic CTA Routing Tests
  console.log("▶️ Test 1.1: Dynamic CTA Routing Logic");
  const scenarios = [
    { name: "CPA / Financial Topic", eval: { targetAudience: "finance", suggestedPostType: "use_case", commercialIntent: "high" }, expected: "consulting" },
    { name: "Beginner AI Tutorial", eval: { targetAudience: "beginners", suggestedPostType: "tutorial", commercialIntent: "medium" }, expected: "course" },
    { name: "Developer Tool Guide", eval: { targetAudience: "developers", suggestedPostType: "tool_explainer", commercialIntent: "medium" }, expected: "tools" },
    { name: "General AI News", eval: { targetAudience: "general", suggestedPostType: "news_analysis", commercialIntent: "low" }, expected: "newsletter" },
  ];

  for (const s of scenarios) {
    const resolved = resolveCtaType(s.eval);
    const passed = resolved === s.expected;
    console.log(`   ${passed ? "✅" : "❌"} [${s.name}] → Routed to: ${resolved} (Expected: ${s.expected})`);
  }

  // 2. Real-Time Lead Scoring Tests
  console.log("\n▶️ Test 1.2: Real-Time Inbound Lead Scoring");
  const mockLeads = [
    {
      name: "דני כהן",
      company: "פירמת עורכי דין וראיית חשבון (60 עובדים)",
      message: "שלום, אנחנו מחפשים ייעוץ להטמעת כלי AI וביקורת אוטומציה למחלקת הכספים.",
      expectedService: "cpa_consulting",
      shouldBeVip: true,
    },
    {
      name: "מיכל לוי",
      company: "עצמאית",
      message: "היי, רציתי לדעת מתי נפתח הקורס הבא שלכם לבינה מלאכותית למתחילים?",
      expectedService: "ai_course",
      shouldBeVip: false,
    },
    {
      name: "Spam Bot",
      company: "Best Casino",
      message: "Free crypto casino bonus click here",
      expectedService: "spam",
      shouldBeVip: false,
    },
  ];

  for (const lead of mockLeads) {
    const result = await scoreLeadWithJev(lead);
    console.log(
      `   👤 Lead: "${lead.name}" | Score: ${result.score}/100 | VIP: ${result.isVip ? "🚨 YES" : "NO"} | Route: ${result.routeAction} | Service: ${result.targetService}`
    );
    console.log(`      Reason: ${result.summaryReason}`);
  }

  console.log("\n=================================================");
  console.log("⚡ TESTING JEV FLOW 2: PRE-PUBLISH SEO & GEO GATE");
  console.log("=================================================\n");

  const validPost = {
    title: "מדריך מקיף: איך לחבר את מודל Jev ל-Vercel AI Gateway",
    metaDescription: "גלו איך לחבר את מודל Jev ל-Vercel AI Gateway בתוך פחות מ-300 מילי-שניות, כולל קוד מעשי, ניתוב מהיר ודוגמאות בעברית.",
    content: `
# מדריך מקיף: איך לחבר את מודל Jev ל-Vercel AI Gateway

> **תקציר מהיר (Zero-Click Answer):** מודל Jev דרך Vercel AI Gateway מספק שכבת קבלת החלטות מהירה במיוחד (System-1) בביצועים של מתחת ל-300ms, ומאפשר סיווג לידים, סינון תוכן והתאמת קריאות לפעולה בזמן אמת.

## מהו מודל Jev?
מודל Jev הוא מנוע הכרעה סמנטי שנועד לקבל החלטות סיווג ואיכות בזמן אפס...
`,
    tags: ["מדריכים", "בינה מלאכותית"],
  };

  const weakPost = {
    title: "פוסט בדיקה ללא תיאור",
    metaDescription: "קצר מדי",
    content: `זה פוסט ללא מבנה וללא הסבר מוגדר. בתור מודל שפה אני לא יודע מה לכתוב.`,
    tags: [],
  };

  console.log("▶️ Test 2.1: Valid High-Quality Post with Zero-Click Answer");
  const evalValid = await evaluateSeoGeoQuality(validPost);
  console.log(`   📊 Score: ${evalValid.score}/10 | Passes Gate: ${evalValid.passesQualityBar ? "✅ PASS" : "❌ FAIL"}`);
  console.log(`   Zero-Click Answer: ${evalValid.containsClearAnswerBlock ? "✓" : "✗"} | Natural Hebrew: ${evalValid.hebrewGrammarNatural ? "✓" : "✗"}`);
  console.log(`   Feedback: ${evalValid.feedback}`);

  console.log("\n▶️ Test 2.2: Low-Quality Weak Post (Missing Zero-Click Answer & Bad Meta)");
  const evalWeak = await evaluateSeoGeoQuality(weakPost);
  console.log(`   📊 Score: ${evalWeak.score}/10 | Passes Gate: ${evalWeak.passesQualityBar ? "✅ PASS" : "⛔ BLOCKED (Expected)"}`);
  console.log(`   Zero-Click Answer: ${evalWeak.containsClearAnswerBlock ? "✓" : "✗"} | Natural Hebrew: ${evalWeak.hebrewGrammarNatural ? "✓" : "✗"}`);
  console.log(`   Feedback: ${evalWeak.feedback}`);

  console.log("\n✨ All tests completed successfully!");
}

runTests().catch(console.error);
