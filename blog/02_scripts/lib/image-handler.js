import fs from "node:fs/promises";
import path from "node:path";

export async function downloadNotionImage(imageFile, slug, publicDir) {
  if (!imageFile) return null;

  const url =
    imageFile.type === "external" ? imageFile.external?.url : imageFile.file?.url;

  if (!url) return null;

  const res = await fetch(url);
  if (!res.ok) throw new Error(`Image download failed: ${res.status}`);

  const buffer = Buffer.from(await res.arrayBuffer());
  const ext = getExtension(url, res.headers.get("content-type"));
  const filename = `${slug}${ext}`;
  const targetDir = path.join(publicDir, "images", "posts");

  await fs.mkdir(targetDir, { recursive: true });
  const fullPath = path.join(targetDir, filename);
  await fs.writeFile(fullPath, buffer);

  return `/images/posts/${filename}`;
}

function getExtension(url, contentType) {
  const fromUrl = path.extname(new URL(url).pathname).toLowerCase();
  if ([".jpg", ".jpeg", ".png", ".webp", ".gif"].includes(fromUrl)) return fromUrl;

  const ct = (contentType || "").toLowerCase();
  if (ct.includes("jpeg") || ct.includes("jpg")) return ".jpg";
  if (ct.includes("png")) return ".png";
  if (ct.includes("webp")) return ".webp";
  if (ct.includes("gif")) return ".gif";
  return ".jpg";
}
