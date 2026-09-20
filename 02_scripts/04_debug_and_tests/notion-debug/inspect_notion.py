import sys
import os
from dotenv import load_dotenv
from notion_client import Client

# Add generator/src to path
sys.path.append(os.path.join(os.getcwd(), 'generator'))

def inspect_notion():
    load_dotenv(dotenv_path="generator/.env")
    token = os.getenv("NOTION_TOKEN")
    id_to_check = os.getenv("NOTION_DATABASE_ID")
    
    client = Client(auth=token)
    
    print(f"Checking ID: {id_to_check}")
    
    try:
        # Try as database
        db = client.databases.retrieve(database_id=id_to_check)
        print("SUCCESS: Found a database!")
        print(f"Title: {db.get('title', [{}])[0].get('plain_text', 'Unknown')}")
    except Exception as e_db:
        print(f"Not a database: {e_db}")
        try:
            # Try as page
            page = client.pages.retrieve(page_id=id_to_check)
            print("SUCCESS: Found a page!")
            
            # List children to find a database
            print("Looking for child databases...")
            children = client.blocks.children.list(block_id=id_to_check)
            for child in children.get("results", []):
                if child["type"] == "child_database":
                    print(f"Found Child Database: {child['child_database']['title']}")
                    print(f"Database ID: {child['id']}")
                elif child["type"] == "child_page":
                    print(f"Found Child Page: {child['child_page']['title']}")
                    print(f"Page ID: {child['id']}")
        except Exception as e_page:
            print(f"Not a page either: {e_page}")

if __name__ == "__main__":
    inspect_notion()
