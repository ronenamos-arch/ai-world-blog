import type { ImageMetadata } from "astro";

const imageModules = import.meta.glob<{ default: ImageMetadata }>(
  "../assets/post-images/*.{jpg,jpeg,png,webp,avif}",
  { eager: true }
);

const postImages = Object.fromEntries(
  Object.entries(imageModules).map(([path, mod]) => [path.split("/").pop()!, mod.default])
) as Record<string, ImageMetadata>;

const imageAliases: Record<string, string> = {
  "claude-agents.jfif": "claude-agents.jpg",
  "resend.jfif": "resend.jpg",
};

export const getOptimizedPostImage = (imagePath?: string | null) => {
  if (!imagePath?.startsWith("/images/posts/")) return null;

  const fileName = decodeURIComponent(imagePath.split("/").pop() ?? "");
  const normalizedName = imageAliases[fileName] ?? fileName;

  return postImages[normalizedName] ?? null;
};
