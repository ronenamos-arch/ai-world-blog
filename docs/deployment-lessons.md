# Deployment Lessons — Known Failures & Pitfalls

This file documents real bugs and deployment failures that occurred in this project, with root causes and fixes. **Read before touching deployment config or content schemas.**

---

## 🔴 Incident: April 2026 — Images 404 + Multiple Build Failures

**Symptoms:**
- Build failed on Vercel repeatedly with different errors
- Images in `public/images/posts/` returned 404 on the live site
- Seemingly unrelated errors each time (`npm install exited with 1`, `ImageNotFound`, etc.)

### Root Cause 1: `vercel.json` overriding correct dashboard settings

**What happened:** The Vercel dashboard already had the correct settings:
- Root Directory: `blog`
- Framework Preset: Astro

A `vercel.json` file was placed at the **repo root** with custom `buildCommand` and `installCommand` values. When Vercel sees a `vercel.json` in the root, it **ignores the dashboard settings** and uses the file instead. The custom commands (`cd blog && npm install`) failed because Vercel's install phase doesn't support `cd` into subdirectories that way.

**Fix:** Delete `vercel.json` entirely. The dashboard settings handle everything correctly.

**Rule going forward:**
> ⚠️ **Do NOT create or edit `vercel.json` in this project.** The Vercel dashboard settings (Root Directory: `blog`, Framework: Astro) are correct and sufficient. A `vercel.json` will override and break them.

---

### Root Cause 2: Astro `image()` schema type used with `public/` images

**What happened:** The content schema in `blog/src/content.config.ts` had:

```ts
ogImage: image().or(z.string()).optional()
```

Astro's `image()` type tells the build to **import and optimize** the file as a build-time asset (like `import img from './my-image.jpg'`). It expects images to be in `src/assets/` or similar.

Our images are in `blog/public/images/posts/` — which are **static files served as-is** at runtime, not build-time assets. When Astro saw a string like `/images/posts/ai-automation-tools.jpg` and tried to import it as a module, it threw:

```
[ImageNotFound] Could not load /images/posts/ai-automation-tools.jpg
```

**Fix:** Change to `z.string()` only:

```ts
ogImage: z.string().optional()
```

**Rule going forward:**
> ⚠️ **Images for blog posts must be either:**
> 1. Placed in `blog/public/images/posts/` and referenced as plain strings (e.g., `/images/posts/my-post.jpg`) — schema must use `z.string()`
> 2. Placed in `blog/src/assets/` and referenced with relative imports — schema can use `image()`
>
> **Never mix:** don't use `image()` schema type with `public/` paths.

---

## Deployment Architecture — Quick Reference

```
Repo root
├── blog/          ← Astro app (Vercel Root Directory points here)
│   ├── public/    ← Static files, served as-is. NOT processed by Astro.
│   │   ├── hero-bg.jpg
│   │   └── images/posts/*.jpg   ← Post thumbnail images go here
│   └── src/
│       ├── assets/  ← Build-time assets (Astro processes these)
│       └── data/blog/*.md  ← Blog posts
└── (no vercel.json)  ← Intentionally absent. Dashboard handles config.
```

**Vercel dashboard settings (do not change):**
- Root Directory: `blog`
- Framework Preset: Astro
- Build Command: default (`pnpm run build` or `npm run build`)
- No overrides needed

---

## Adding Images to New Posts

When the generator pipeline adds a new post with an image:

1. **Save JP/PNG** to `blog/public/images/posts/<slug>.jpg`
2. **Set frontmatter** as a plain string:
   ```yaml
   ogImage: /images/posts/<slug>.jpg
   ```
3. **Do NOT** use a local relative path like `./images/foo.jpg` — use the absolute public path starting with `/`
4. The schema is `z.string()` — no Astro image processing happens. The file is served directly.
