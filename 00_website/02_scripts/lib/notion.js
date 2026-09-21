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
      prompt: p["origin post "]?.rich_text?.map((r) => r.plain_text).join("") || "",
      urlSource: p["URL מקור"]?.url || "",
      finalPost: p["הפוסט הסופי"]?.rich_text?.map((r) => r.plain_text).join("") || "",
      category: p["קטגוריה"]?.multi_select?.map((s) => s.name) || [],
      score: p["ניקוד"]?.number || null,
      image: p["תמונה שנוצרה"]?.files?.[0] || null,
      status: p.Status?.status?.name || "",
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

  async setFields(pageId, { metaDescription, score, postLink, publishedDate }) {
    const props = {};
    if (metaDescription) {
      props["Meta Description"] = {
        rich_text: [{ text: { content: metaDescription.slice(0, 2000) } }],
      };
    }
    if (typeof score === "number") {
      props["ניקוד"] = { number: score };
    }
    if (postLink) {
      props["לינק לפוסט"] = { url: postLink };
    }
    if (publishedDate) {
      props["תאריך פרסום"] = { date: { start: publishedDate } };
    }
    if (Object.keys(props).length === 0) return;
    return this.updatePage(pageId, props);
  }

  async setCategories(pageId, categoryNames) {
    if (!categoryNames || categoryNames.length === 0) return;
    try {
      return await this.updatePage(pageId, {
        "קטגוריה": {
          multi_select: categoryNames.map((name) => ({ name })),
        },
      });
    } catch (e) {
      console.warn(`   ⚠️ Could not update Notion category: ${e.message}`);
    }
  }

  async addComment(pageId, message) {
    try {
      return await this.client.comments.create({
        parent: { page_id: pageId },
        rich_text: [
          {
            text: {
              content: message,
            },
          },
        ],
      });
    } catch (e) {
      console.warn(`   ⚠️ Could not add Notion comment: ${e.message}`);
    }
  }

  async recordJevEvaluation(pageId, jevEval) {
    const statusNote = jevEval.passed ? "מאושר לפרסום ✅" : "נדחה באיכות נמוכה ❌";
    const comment = `⚡ הערכת Jev System-1 Triage:
• ציון איכות: ${jevEval.qualityScore}/10 (${statusNote})
• סוג פוסט מומלץ: ${jevEval.suggestedPostType}
• קהל יעד עיקרי: ${jevEval.targetAudience}
• קריאה לפעולה (CTA): ${jevEval.recommendedCta} (כוונה מסחרית: ${jevEval.commercialIntent})
• נימוק עריכה: ${jevEval.summaryReason}`;

    // Update Score in Notion column
    if (typeof jevEval.qualityScore === "number") {
      await this.setFields(pageId, { score: jevEval.qualityScore });
    }

    // Add rich comment in Notion
    await this.addComment(pageId, comment);

    // Auto-tag categories
    if (jevEval.categories && jevEval.categories.length > 0) {
      await this.setCategories(pageId, jevEval.categories);
    }
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
