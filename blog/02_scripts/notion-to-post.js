import "dotenv/config";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { NotionBlog } from "./lib/notion.js";
import { generatePost } from "./lib/ai-generator.js";
import { evaluateStoryWithJev } from "./lib/jev-evaluator.js";
import { injectDynamicCta } from "./lib/cta-manager.js";
import { downloadNotionImage } from "./lib/image-handler.js";
import { scrapeUrl } from "./lib/url-scraper.js";
import { writePostMarkdown } from "./lib/markdown-writer.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const BLOG_ROOT = path.resolve(__dirname, "..");
const BLOG_POSTS_DIR = path.join(BLOG_ROOT, "src", "data", "blog");
const PUBLIC_DIR = path.join(BLOG_ROOT, "public");
const AUTHOR = process.env.BLOG_AUTHOR || "מומחה ה AI שלכם";

async function main() {
  console.log("🔍 Fetching entries with Status = 'ready to publish'...\n");

  const notion = new NotionBlog(
    process.env.NOTION_TOKEN,
    process.env.NOTION_DATABASE_ID
  );

  const pages = await notion.getPagesByStatus("ready to publish");

  if (pages.length === 0) {
    console.log("✅ No entries to process. All caught up!");
    return;
  }

  console.log(`📝 Found ${pages.length} entries to process\n`);

  let successCount = 0;
  let skippedCount = 0;
  let errorCount = 0;

  for (const page of pages) {
    const fields = notion.extractFields(page);
    console.log(`\n▶️  Processing: "${fields.name}"`);

    try {
      // Skip if both prompt and URL are empty
      if (!fields.prompt && !fields.urlSource && !fields.finalPost) {
        console.log("   ⏭️  Skipped: no content source");
        continue;
      }

      // Scrape URL if present
      let scrapedContent = null;
      if (fields.urlSource) {
        console.log(`   🌐 Scraping ${fields.urlSource}...`);
        scrapedContent = await scrapeUrl(fields.urlSource);
      }

      // System 1 Jev Pre-Flight Gate & Triage (Phases 1 & 2)
      console.log("   ⚡ Evaluating candidate with Jev (System-1 Pre-Flight & Triage)...");
      const jevEval = await evaluateStoryWithJev({
        name: fields.name,
        prompt: fields.prompt,
        urlSource: fields.urlSource,
        scrapedContent,
      });

      console.log(
        `   📊 Jev Score: ${jevEval.qualityScore}/10 | Type: ${jevEval.suggestedPostType} | Audience: ${jevEval.targetAudience} | CTA: ${jevEval.recommendedCta} (${jevEval.durationMs || 0}ms)`
      );

      // Record Jev evaluation comment & category triage in Notion
      await notion.recordJevEvaluation(page.id, jevEval);
      console.log("   📝 Recorded Jev evaluation note & categories in Notion");

      if (!jevEval.passed) {
        console.log(`   ⛔ Post deferred by Jev gate: ${jevEval.summaryReason}`);
        await notion.setStatus(page.id, "נדחה באיכות נמוכה");
        skippedCount++;
        continue;
      }

      // Generate full Hebrew post with Claude (informed by Jev triage)
      console.log("   🤖 Generating post with Claude...");
      const post = await generatePost({
        name: fields.name,
        prompt: fields.prompt,
        urlSource: fields.urlSource,
        partialContent: fields.finalPost,
        scrapedContent,
        jevContext: jevEval,
      });

      // Phase 3: Dynamic Monetization CTA Injection
      const postContentWithCta = injectDynamicCta(post.content, jevEval);
      const wordCount = postContentWithCta.split(/\s+/).filter(Boolean).length;
      console.log(`   💰 Attached High-Converting CTA: [${jevEval.recommendedCta}]`);
      console.log(`   ✍️  Generated: "${post.title}" (${wordCount} words)`);

      // Handle image
      let ogImage = null;
      if (fields.image) {
        console.log("   🖼️  Downloading image...");
        ogImage = await downloadNotionImage(fields.image, post.slug, PUBLIC_DIR);
        console.log(`   ✅ Image saved: ${ogImage}`);
      } else {
        console.log("   ⚠️  No image in Notion - post will have no OG image");
      }

      // Write markdown file (as draft)
      const { filePath, filename } = await writePostMarkdown({
        blogDir: BLOG_POSTS_DIR,
        slug: post.slug,
        title: post.title,
        description: post.description,
        author: AUTHOR,
        tags: post.tags,
        content: postContentWithCta,
        ogImage,
        draft: true,
      });

      console.log(`   📄 Created: ${filename}`);

      // Update Notion with final post, SEO metadata, and word count
      await notion.setFinalPost(page.id, postContentWithCta);
      await notion.setFields(page.id, {
        slug: post.slug,
        metaDescription: post.description,
        altText: post.altText,
        wordCount: wordCount,
      });

      // Set status based on image presence
      const nextStatus = fields.image ? "In progress" : "ממתין לתמונה";
      await notion.setStatus(page.id, nextStatus);
      console.log(`   ✅ Notion updated → Status: ${nextStatus}`);

      successCount++;
    } catch (e) {
      console.error(`   ❌ Error: ${e.message}`);
      try {
        await notion.logError(page.id, e.message);
      } catch (_) {
        /* ignore logging failure */
      }
      errorCount++;
    }
  }

  console.log(`\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
  console.log(
    `✨ Done! ${successCount} succeeded, ${skippedCount} skipped by Jev, ${errorCount} failed`
  );
  console.log(`\n📋 NEXT STEPS:`);
  console.log(`1. Run 'npm run dev' to preview locally at http://localhost:4321`);
  console.log(`2. Review generated posts (they have draft: true)`);
  console.log(`3. In Notion: tick ☑ "ביקורת אנושית" for approved posts`);
  console.log(`4. Run 'npm run publish' to deploy to production`);
}

main().catch((e) => {
  console.error("💥 Fatal error:", e);
  process.exit(1);
});
