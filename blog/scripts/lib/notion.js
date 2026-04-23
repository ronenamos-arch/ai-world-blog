import { Client } from "@notionhq/client";

export class NotionBlog {
  constructor(token, databaseId) {
    this.client = new Client({ auth: token });
    this.databaseId = databaseId;
    this.dataSourceId = null;
  }

  async getDataSourceId() {
    if (this.dataSourceId) return this.dataSourceId;
    const db = await this.client.databases.retrieve({ database_id: this.databaseId });
    this.dataSourceId = db.data_sources?.[0]?.id;
    return this.dataSourceId;
  }

  async getPagesByStatus(statusValue) {
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

    return (data.results || []).filter((p) => {
      const parentOk = p.parent?.database_id === this.databaseId;
      const status = p.properties?.Status?.status?.name;
      return parentOk && status === statusValue;
    });
  }

  async getPagesReviewed() {
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

    return (data.results || []).filter((p) => {
      const parentOk = p.parent?.database_id === this.databaseId;
      const status = p.properties?.Status?.status?.name;
      const reviewed = p.properties?.["ביקורת אנושית"]?.checkbox === true;
      return parentOk && status === "In progress" && reviewed;
    });
  }

  extractFields(page) {
    const p = page.properties;
    return {
      id: page.id,
      name: p.Name?.title?.[0]?.plain_text || "",
      prompt: p.Prompt?.rich_text?.map((r) => r.plain_text).join("") || "",
      urlSource: p["URL מקור"]?.url || "",
      finalPost: p["הפוסט הסופי"]?.rich_text?.map((r) => r.plain_text).join("") || "",
      category: p["קטגוריה"]?.multi_select?.map((s) => s.name) || [],
      image: p["תמונה שנוצרה"]?.files?.[0] || null,
      status: p.Status?.status?.name || "",
      slug: p.Slug?.rich_text?.[0]?.plain_text || "",
    };
  }

  async updatePage(pageId, properties) {
    return this.client.pages.update({ page_id: pageId, properties });
  }

  async setStatus(pageId, status) {
    return this.updatePage(pageId, {
      Status: { status: { name: status } },
    });
  }

  async setFinalPost(pageId, content) {
    // Notion has a 2000 char limit per rich_text block; chunk if needed
    const chunks = [];
    for (let i = 0; i < content.length; i += 2000) {
      chunks.push({ type: "text", text: { content: content.slice(i, i + 2000) } });
    }
    return this.updatePage(pageId, {
      "הפוסט הסופי": { rich_text: chunks },
    });
  }

  async setFields(pageId, { slug, metaDescription, altText, wordCount, postLink, publishedDate }) {
    const props = {};
    if (slug) props.Slug = { rich_text: [{ text: { content: slug } }] };
    if (metaDescription)
      props["Meta Description"] = { rich_text: [{ text: { content: metaDescription } }] };
    if (altText) props["Alt Text"] = { rich_text: [{ text: { content: altText } }] };
    if (wordCount !== undefined) props["מילים"] = { number: wordCount };
    if (postLink) props["לינק לפוסט"] = { url: postLink };
    if (publishedDate)
      props["תאריך פרסום"] = { date: { start: publishedDate } };
    return this.updatePage(pageId, props);
  }

  async setPublished(pageId) {
    return this.updatePage(pageId, {
      Status: { status: { name: "published" } },
      "פורסם באתר": { checkbox: true },
    });
  }

  async logError(pageId, message) {
    return this.updatePage(pageId, {
      Status: { status: { name: "Error" } },
      "הפוסט הסופי": {
        rich_text: [{ text: { content: `[ERROR] ${message}`.slice(0, 2000) } }],
      },
    });
  }
}
