from notion_client import Client
import os
from dotenv import load_dotenv

def list_pages():
    load_dotenv(dotenv_path="generator/.env")
    token = os.getenv("NOTION_TOKEN")
    db_id = os.getenv("NOTION_DATABASE_ID")
    client = Client(auth=token)
    
    print(f"Listing pages in database: {db_id}")
    try:
        response = client.request(
            path=f"databases/{db_id}/query",
            method="POST",
            body={} # No filter
        )
        results = response.get("results", [])
        print(f"Total results: {len(results)}")
        for page in results:
            props = page.get("properties", {})
            title_prop = props.get("Name") or props.get("title") or props.get("URL")
            print(f"- Page ID: {page['id']}")
            print(f"  Properties found: {list(props.keys())}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_pages()
