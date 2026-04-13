from notion_client import Client
import os
from dotenv import load_dotenv
import json

def inspect_page():
    load_dotenv(dotenv_path="generator/.env")
    token = os.getenv("NOTION_TOKEN")
    ds_id = os.getenv("NOTION_DATABASE_ID")
    client = Client(auth=token)
    
    response = client.data_sources.query(data_source_id=ds_id, page_size=1)
    results = response.get("results", [])
    if results:
        page = results[0]
        print(json.dumps(page["properties"], indent=2, ensure_ascii=False))

if __name__ == "__main__":
    inspect_page()
