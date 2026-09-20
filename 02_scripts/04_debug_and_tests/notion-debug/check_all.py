from notion_client import Client
import os
from dotenv import load_dotenv

def check_all_statuses():
    load_dotenv(dotenv_path="generator/.env")
    token = os.getenv("NOTION_TOKEN")
    ds_id = os.getenv("NOTION_DATABASE_ID")
    client = Client(auth=token)
    
    response = client.data_sources.query(data_source_id=ds_id)
    results = response.get("results", [])
    print(f"Total pages: {len(results)}")
    for res in results:
        props = res.get("properties", {})
        status = props.get("Status", {}).get("status", {}).get("name", "Unknown")
        name = "Untitled"
        title_list = props.get("Name", {}).get("title", [])
        if title_list:
            name = title_list[0].get("plain_text", "Untitled")
        print(f"- {name} | Status: {status}")

if __name__ == "__main__":
    check_all_statuses()
