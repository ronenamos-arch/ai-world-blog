# Connecting Your Blog to Notion

Your blog generator is now integrated with Notion! This allows you to manage your article queue in a collaborative Notion database.

## 1. Setup Notion Database

Create a new Database in Notion with the following columns:

| Property Name | Type | Description |
| :--- | :--- | :--- |
| **Name** | Title | The topic or name of the article |
| **URL** | URL | The source URL to scrape/process (Mandatory) |
| **Status** | Status | Options: `Pending`, `Processing`, `Published`, `Error` |
| **Priority** | Number | 1 is highest priority. Generator picks the lowest number. |
| **Type** | Select | Options: `tool_explainer`, `tutorial`, `comparison`, `use_case` |
| **Tags** | Multi-select | Any tags you want to include in the frontmatter |

> [!IMPORTANT]
> The database **must** have a property named `Status` (Status type) and `URL` (URL type). 
> The code specifically looks for rows where `Status == Pending`.

## 2. Generate Notion Credentials

1. Go to [Notion Integrations](https://www.notion.com/my-integrations).
2. Create a new "Internal Integration".
3. Copy the **Internal Integration Token**.
4. Go to your Notion Database page.
5. Click the "..." (top right) -> **Connect to** -> Search for your integration name.

## 3. Update `.env`

Add these variables to your `generator/.env` file:

```env
NOTION_TOKEN=secret_your_token_here
NOTION_DATABASE_ID=your_database_id_here
```

*To find your Database ID:* Open the database in your browser. The ID is the part of the URL after the workspace name (or `notion.so/`) and before the `?v=...`. It is a 32-character alphanumeric string.

## 4. How to Use

Simply run the generator with the `--next` flag:

```bash
python -m src.cli --next
```

The generator will:
1. Check Notion for the next `Pending` article.
2. If found, it will process it.
3. Once finished, it will update that article's status in Notion to `Published`.
4. If Notion credentials are missing, it will automatically fall back to `state/queue.yaml`.
