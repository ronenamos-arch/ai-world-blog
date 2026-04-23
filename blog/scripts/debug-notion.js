import "dotenv/config";

const res = await fetch("https://api.notion.com/v1/search", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${process.env.NOTION_TOKEN}`,
    "Notion-Version": "2025-09-03",
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ page_size: 100 }),
});
const data = await res.json();

const pages = (data.results || []).filter(
  (p) => p.parent?.database_id === process.env.NOTION_DATABASE_ID
);

console.log(`\nFound ${pages.length} pages in database.\n`);

for (const p of pages) {
  const name =
    p.properties?.Name?.title?.[0]?.plain_text ||
    p.properties?.Name?.title?.map((t) => t.plain_text).join("") ||
    "(no name)";
  const status = p.properties?.Status?.status?.name || "(no status)";

  const checkboxKeys = Object.keys(p.properties).filter(
    (k) => p.properties[k].type === "checkbox"
  );

  const checkboxes = checkboxKeys
    .map((k) => `"${k}"=${p.properties[k].checkbox}`)
    .join(" | ");

  console.log(`• ${name}`);
  console.log(`    Status: ${status}`);
  console.log(`    Checkboxes: ${checkboxes || "(none)"}`);
}
