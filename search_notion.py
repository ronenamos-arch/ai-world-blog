import sys
import os
from dotenv import load_dotenv
from notion_client import Client

def search_notion():
    load_dotenv(dotenv_path="generator/.env")
    token = os.getenv("NOTION_TOKEN")
    client = Client(auth=token)
    
    print("Searching for databases accessible to this integration...")
    try:
        # Search without filter, then filter locally
        results = client.search().get("results", [])
        found = False
        for obj in results:
            if obj["object"] == "database":
                found = True
                title = obj.get('title', [{}])[0].get('plain_text', 'Untitled')
                print(f"Database Title: {title}")
                print(f"Database ID: {obj['id'].replace('-', '')}")
                print("-" * 20)
        
        if not found:
            print("No databases found. Make sure you shared the database with the integration.")
            print("Accessible objects found:")
            for obj in results:
                title = "Unknown"
                if obj["object"] == "page":
                    # Pages title is in properties
                    props = obj.get("properties", {})
                    for p in props.values():
                        if p["type"] == "title":
                            title = p["title"][0]["plain_text"] if p["title"] else "Untitled"
                print(f"- {obj['object']}: {title} (ID: {obj['id']})")

    except Exception as e:
        print(f"Error during search: {e}")

if __name__ == "__main__":
    search_notion()
