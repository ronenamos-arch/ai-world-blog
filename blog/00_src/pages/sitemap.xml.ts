import type { APIRoute } from "astro";

export const GET: APIRoute = ({ site }) => {
  const sitemapURL = new URL("sitemap-index.xml", site);
  return new Response(null, {
    status: 301,
    headers: {
      Location: sitemapURL.href,
    },
  });
};
