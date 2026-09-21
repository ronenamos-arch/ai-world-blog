import fs from "node:fs/promises";
import path from "node:path";

export async function writePostMarkdown({
  blogDir,
  slug,
  title,
  description,
  author,
  tags,
  content,
  ogImage,
  draft = true,
}) {
  const now = new Date();
  const isoLocal = toIsoWithOffset(now);
  const datePart = now.toISOString().slice(0, 10); // YYYY-MM-DD
  const filename = `${datePart}-${slug}.md`;

  const frontmatter = [
    "---",
    `title: "${escape(title)}"`,
    `description: "${escape(description)}"`,
    `pubDatetime: ${isoLocal}`,
    `author: ${author}`,
    "tags:",
    ...tags.map((t) => `  - ${t}`),
    `featured: false`,
    `draft: ${draft}`,
    ogImage ? `ogImage: ${ogImage}` : null,
    "---",
    "",
  ]
    .filter(Boolean)
    .join("\n");

  const body = frontmatter + "\n" + content.trim() + "\n";
  const targetPath = path.join(blogDir, filename);

  await fs.writeFile(targetPath, body, "utf-8");
  return { filePath: targetPath, filename };
}

export async function setDraftFalse(filePath) {
  const content = await fs.readFile(filePath, "utf-8");
  const updated = content.replace(/^draft:\s*true\s*$/m, "draft: false");
  if (updated === content) return false;
  await fs.writeFile(filePath, updated, "utf-8");
  return true;
}

function escape(str) {
  return String(str || "").replace(/"/g, '\\"');
}

function toIsoWithOffset(date) {
  const pad = (n) => String(n).padStart(2, "0");
  const tzOffset = -date.getTimezoneOffset();
  const sign = tzOffset >= 0 ? "+" : "-";
  const abs = Math.abs(tzOffset);
  const tz = `${sign}${pad(Math.floor(abs / 60))}:${pad(abs % 60)}`;
  return (
    `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}` +
    `T${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}${tz}`
  );
}
