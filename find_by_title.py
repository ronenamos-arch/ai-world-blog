from notion_client import Client
import os
from dotenv import load_dotenv

def find_by_title():
    load_dotenv(dotenv_path="generator/.env")
    token = os.getenv("NOTION_TOKEN")
    client = Client(auth=token)
    
    print("Searching for 'תוכן לאתר AI-WORLD-BLOG'...")
    try:
        results = client.search(query="תוכן לאתר AI-WORLD-BLOG").get("results", [])
        for obj in results:
            print(f"Object: {obj['object']} | ID: {obj['id']} | Title: {obj.get('title', [{}])[0].get('plain_text', 'Untitled')}")
            if obj['object'] == 'database':
                print(f"  --> USE THIS DATABASE ID: {obj['id'].replace('-', '')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    find_by_title()
