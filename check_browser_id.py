import sys
import os
from dotenv import load_dotenv
from notion_client import Client

def check_specific_id():
    load_dotenv(dotenv_path="generator/.env")
    token = os.getenv("NOTION_TOKEN")
    client = Client(auth=token)
    
    # ID from browser state
    db_id = "33d927f0e15480ed8e8ad00e60e47fbb"
    
    try:
        db = client.databases.retrieve(database_id=db_id)
        print("SUCCESS! Found database via browser ID.")
        print(f"Title: {db.get('title', [{}])[0].get('plain_text')}")
    except Exception as e:
        print(f"Failed to find database with ID {db_id}: {e}")

if __name__ == "__main__":
    check_specific_id()
