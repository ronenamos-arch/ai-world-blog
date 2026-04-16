from notion_client import Client
import os
from dotenv import load_dotenv

def get_final_post():
    load_dotenv(dotenv_path="generator/.env")
    token = os.getenv("NOTION_TOKEN")
    ds_id = os.getenv("NOTION_DATABASE_ID")
    client = Client(auth=token)
    
    response = client.data_sources.query(data_source_id=ds_id)
    results = response.get("results", [])
    for res in results:
        props = res.get("properties", {})
        name_list = props.get("Name", {}).get("title", [])
        if name_list and "פגישות" in name_list[0].get("plain_text", ""):
            # Found it!
            final_post_list = props.get("הפוסט הסופי", {}).get("rich_text", [])
            content = "".join([t.get("plain_text", "") for t in final_post_list])
            
            print(f"TITLE: {name_list[0].get('plain_text')}")
            print(f"PAGE_ID: {res['id']}")
            print("---CONTENT START---")
            print(content)
            print("---CONTENT END---")
            
            # Also get other props
            tags_prop = props.get("קטגוריה", {})
            tags = [t["name"] for t in tags_prop.get("multi_select", [])] if tags_prop.get("type") == "multi_select" else []
            print(f"TAGS: {tags}")

if __name__ == "__main__":
    get_final_post()
