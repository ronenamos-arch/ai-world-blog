from notion_client import Client
import os
from dotenv import load_dotenv

def check_type():
    load_dotenv(dotenv_path="generator/.env")
    token = os.getenv("NOTION_TOKEN")
    db_id = os.getenv("NOTION_DATABASE_ID")
    client = Client(auth=token)
    
    print(f"Retrieving database: {db_id}")
    try:
        db = client.databases.retrieve(database_id=db_id)
        print(f"Object type: {db.get('object')}")
        print(f"Properties: {list(db.get('properties', {}).keys())}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_type()
