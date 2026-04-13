import sys
import os
from dotenv import load_dotenv
from notion_client import Client

def find_database():
    load_dotenv(dotenv_path="generator/.env")
    token = os.getenv("NOTION_TOKEN")
    client = Client(auth=token)
    
    print("Listing all accessible objects and checking if they are databases...")
    try:
        results = client.search().get("results", [])
        for obj in results:
            obj_id = obj["id"]
            obj_type = obj["object"]
            
            title = "Untitled"
            if obj_type == "database":
                title = obj.get('title', [{}])[0].get('plain_text', 'Untitled')
                print(f"FOUND DATABASE: {title} | ID: {obj_id.replace('-', '')}")
            elif obj_type == "page":
                props = obj.get("properties", {})
                for p in props.values():
                    if p["type"] == "title":
                        title = p["title"][0]["plain_text"] if p["title"] else "Untitled"
                print(f"FOUND PAGE: {title} | ID: {obj_id.replace('-', '')}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    find_database()
