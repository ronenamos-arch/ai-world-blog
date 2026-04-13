import sys
import os
from dotenv import load_dotenv
from notion_client import Client

def check_parent():
    load_dotenv(dotenv_path="generator/.env")
    token = os.getenv("NOTION_TOKEN")
    client = Client(auth=token)
    
    # ID of one of the posts we found
    post_id = "33e927f0e154801dbebcc803ddef4fd1"
    
    try:
        page = client.pages.retrieve(page_id=post_id)
        parent = page.get("parent", {})
        print(f"Parent Type: {parent.get('type')}")
        if parent.get('type') == 'database_id':
            print(f"FOUND DATABASE ID: {parent['database_id'].replace('-', '')}")
        else:
            print(f"Parent ID: {parent.get('page_id') or parent.get('block_id')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_parent()
