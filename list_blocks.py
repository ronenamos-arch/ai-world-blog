import sys
import os
from dotenv import load_dotenv
from notion_client import Client

def list_page_content():
    load_dotenv(dotenv_path="generator/.env")
    token = os.getenv("NOTION_TOKEN")
    page_id = os.getenv("NOTION_DATABASE_ID")
    client = Client(auth=token)
    
    print(f"Listing blocks for page ID: {page_id}")
    try:
        blocks = client.blocks.children.list(block_id=page_id).get("results", [])
        for block in blocks:
            print(f"Block Type: {block['type']} | ID: {block['id']}")
            if block['type'] == 'child_database':
                print(f"  --> DATABASE TITLE: {block['child_database']['title']}")
                print(f"  --> DATABASE ID: {block['id'].replace('-', '')}")
            if block['type'] == 'child_page':
                print(f"  --> PAGE TITLE: {block['child_page']['title']}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_page_content()
