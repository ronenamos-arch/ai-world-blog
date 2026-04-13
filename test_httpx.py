import httpx
import os
from dotenv import load_dotenv

def test_httpx():
    load_dotenv(dotenv_path="generator/.env")
    token = os.getenv("NOTION_TOKEN")
    db_id = os.getenv("NOTION_DATABASE_ID")
    
    url = f"https://api.notion.com/v1/databases/{db_id}/query"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28", # Try a standard version
        "Content-Type": "application/json"
    }
    
    print(f"URL: {url}")
    try:
        response = httpx.post(url, headers=headers, json={})
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_httpx()
