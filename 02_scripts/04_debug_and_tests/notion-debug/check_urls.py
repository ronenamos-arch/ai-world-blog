from notion_client import Client
import os
from dotenv import load_dotenv

def check_urls():
    load_dotenv(dotenv_path="generator/.env")
    token = os.getenv("NOTION_TOKEN")
    ds_id = os.getenv("NOTION_DATABASE_ID")
    client = Client(auth=token)
    
    response = client.data_sources.query(data_source_id=ds_id)
    results = response.get("results", [])
    for res in results:
        props = res.get("properties", {})
        status_data = props.get("Status", {}).get("status")
        status = status_data.get("name", "Unknown") if status_data else "Unknown"
        
        title_list = props.get("Name", {}).get("title", [])
        name = title_list[0].get("plain_text", "Untitled") if title_list else "Untitled"
        
        url_data = props.get("URL מקור", {})
        url = url_data.get("url") if url_data else None
        
        print(f"- {name} | Status: {status} | URL: {url}")

if __name__ == "__main__":
    check_urls()
