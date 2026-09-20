import "dotenv/config";
import path from "node:path";
import fs from "node:fs/promises";
import { fileURLToPath } from "node:url";

import { NotionBlog } from "./lib/notion.js";
import { setDraftFalse } from "./lib/markdown-writer.js";
import { commitAndPush } from "./lib/git-publisher.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const BLOG_ROOT = path.resolve(__dirname, "..");
const REPO_ROOT = path.resolve(BLOG_ROOT, "..");
const BLOG_POSTS_DIR = path.join(BLOG_ROOT, "src", "data", "blog");
const SITE_BASE = "https://ai-world-blog.vercel.app/posts/";

async function main() {
  console.log("🔍 Fetching reviewed entries (Status = 'In progress' + ביקורת אנושית ✓)...\n");

  const notion = new NotionBlog(
    process.env.NOTION_TOKEN,
    process.env.NOTION_DATABASE_ID
  );

  const pages = await notion.getPagesReviewed();

  if (pages.length === 0) {
    console.log("✅ No approved posts pending publication.");
    console.log('   (Tick "ביקורת אנושית" in Notion first)');
    return;
  }

  console.log(`📤 Found ${pages.length} approved post(s) to publish\n`);

  const publishedFiles = [];
  const publishedPages = [];

  for (const page of pages) {
    const fields = notion.extractFields(page);
    console.log(`\n▶️  Publishing: "${fields.name}"`);

    try {
      if (!fields.slug) {
        throw new Error("Slug is empty — cannot locate markdown file");
      }

      // Find the markdown file by slug
      const files = await fs.readdir(BLOG_POSTS_DIR);
      const match = files.find((f) => f.endsWith(`${fields.slug}.md`));
      if (!match) {
        throw new Error(`Markdown file not found for slug: ${fields.slug}`);
      }
      const filePath = path.join(BLOG_POSTS_DIR, match);

      // Flip draft: true → false
      const changed = await setDraftFalse(filePath);
      if (!changed) {
        console.log("   ℹ️  Already published (draft was not true)");
      } else {
        console.log(`   ✅ Set draft: false in ${match}`);
      }

      publishedFiles.push(filePath);
      publishedPages.push({ page, fields, filename: match });
    } catch (e) {
      console.error(`   ❌ Error: ${e.message}`);
      try {
        await notion.logError(page.id, e.message);
      } catch (_) {}
    }
  }

  if (publishedFiles.length === 0) {
    console.log("\n⚠️  Nothing to publish.");
    return;
  }

  // Commit and push
  console.log(`\n📦 Committing ${publishedFiles.length} file(s) to git...`);
  try {
    const message = `Publish ${publishedFiles.length} post(s) from Notion\n\n${publishedPages
      .map((p) => `- ${p.fields.name}`)
      .join("\n")}`;

    const result = commitAndPush(REPO_ROOT, publishedFiles, message);

    if (!result.committed) {
      console.log(`   ℹ️  ${result.reason}`);
    } else {
      console.log(`   ✅ Pushed commit ${result.sha.slice(0, 7)}`);
    }

    // Update Notion
    const todayIso = new Date().toISOString().slice(0, 10);
    for (const { page, fields } of publishedPages) {
      const postUrl = SITE_BASE + new Date().toISOString().slice(0, 10) + "-" + fields.slug;
      await notion.setFields(page.id, {
        postLink: postUrl,
        publishedDate: todayIso,
      });
      await notion.setPublished(page.id);
      console.log(`   ✅ Notion updated: ${fields.name} → published`);
    }
  } catch (e) {
    console.error(`💥 Git publish failed: ${e.message}`);
    console.log("\n   Your markdown files are updated but not pushed.");
    console.log("   You can push manually: git add, git commit, git push");
    process.exit(1);
  }

  console.log(`\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
  console.log(`✨ Published ${publishedFiles.length} post(s)!`);
  console.log(`🚀 Vercel will deploy in ~1-2 min: https://ai-world-blog.vercel.app`);
}

main().catch((e) => {
  console.error("💥 Fatal error:", e);
  process.exit(1);
});
