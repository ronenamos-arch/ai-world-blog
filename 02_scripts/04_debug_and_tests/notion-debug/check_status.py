from notion_client import Client
import os
from dotenv import load_dotenv

def check_status_options():
    load_dotenv(dotenv_path="generator/.env")
    token = os.getenv("NOTION_TOKEN")
    ds_id = os.getenv("NOTION_DATABASE_ID")
    client = Client(auth=token)
    
    ds = client.data_sources.retrieve(data_source_id=ds_id)
    status_prop = ds.get("properties", {}).get("Status", {})
    if status_prop.get("type") == "status":
        options = status_prop.get("status", {}).get("options", [])
        print("Status Options:")
        for opt in options:
            print(f"- {opt['name']}")
    else:
        print("Status property not found or not a status type.")

if __name__ == "__main__":
    check_status_options()
