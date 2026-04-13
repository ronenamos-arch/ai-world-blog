from notion_client import Client
import os
from dotenv import load_dotenv

def test_raw_query():
    load_dotenv(dotenv_path="generator/.env")
    token = os.getenv("NOTION_TOKEN")
    db_id = os.getenv("NOTION_DATABASE_ID")
    client = Client(auth=token)
    
    print(f"Testing raw query on ID: {db_id}")
    try:
        response = client.request(
            path=f"databases/{db_id}/query",
            method="POST",
            body={
                "filter": {
                    "property": "Status",
                    "status": {
                        "equals": "Pending"
                    }
                }
            }
        )
        results = response.get("results", [])
        print(f"SUCCESS! Found {len(results)} pending articles.")
        for page in results:
            url = page.get('properties', {}).get('URL', {}).get('url')
            title = page.get('properties', {}).get('Name', {}).get('title', [{}])[0].get('plain_text', 'Untitled')
            print(f"- {title}: {url}")
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    test_raw_query()
