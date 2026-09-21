import "dotenv/config";
import { evaluateStoryWithJev } from "./lib/jev-evaluator.js";

async function runTests() {
  console.log("🧪 Starting Jev System-1 Pre-Flight Evaluation Tests...\n");

  const testCandidates = [
    {
      title: "Case 1: High-Value Tech / AI Tool Guide",
      input: {
        name: "מדריך מעשי ל-Claude Code ואוטומציה של פיתוח",
        prompt: "איך להשתמש ב-Claude Code CLI לבניית סוכני AI עצמאיים ולחסוך שעות פיתוח למתכנתים",
        urlSource: "https://anthropic.com/claude-code",
      },
    },
    {
      title: "Case 2: Business & Finance AI Automation (Consulting Lead Magnet)",
      input: {
        name: "אוטומציה של ניהול כספים וחשבוניות באמצעות בינה מלאכותית",
        prompt: "איך רואי חשבון ומנהלי כספים בישראל יכולים לחסוך 80% מהזמן בקריאת דוחות כספיים עם מודלי שפה",
        urlSource: "https://ronenamoscpa.co.il",
      },
    },
    {
      title: "Case 3: Low-Quality / Irrelevant Content (Should be Rejected)",
      input: {
        name: "קניית עוקבים באינסטגרם בהנחה מיוחדת",
        prompt: "איך להשיג 10,000 עוקבים מזויפים תוך 5 דקות ללא מאמץ",
        urlSource: "",
      },
    },
  ];

  for (const test of testCandidates) {
    console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
    console.log(`📌 ${test.title}`);
    console.log(`   Input: "${test.input.name}"`);

    const result = await evaluateStoryWithJev(test.input);

    console.log(`\n   ⚡ Evaluation Result:`);
    console.log(`   • Passed Pre-Flight Gate: ${result.passed ? "✅ YES" : "❌ NO (Skipped)"}`);
    console.log(`   • Quality Score:          ${result.qualityScore}/10`);
    console.log(`   • Target Audience:        ${result.targetAudience}`);
    console.log(`   • Post Type:              ${result.suggestedPostType}`);
    console.log(`   • Commercial Intent:      ${result.commercialIntent}`);
    console.log(`   • Recommended CTA:        ${result.recommendedCta}`);
    console.log(`   • Summary Reasoning:      ${result.summaryReason}`);
    console.log(`   • Response Latency:       ${result.durationMs ? result.durationMs + "ms" : "N/A"}\n`);
  }

  console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
  console.log(`✨ All test scenarios evaluated successfully!\n`);
}

runTests().catch((err) => {
  console.error("Test runner failed:", err);
});
