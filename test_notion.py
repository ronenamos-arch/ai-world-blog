import sys
import os
from dotenv import load_dotenv

# Add generator/src to path
sys.path.append(os.path.join(os.getcwd(), 'generator'))

from generator.src.notion_client import NotionClient

def test_notion():
    print("Testing Notion connection...")
    client = NotionClient()
    if not client.client:
        print("FAILED: Notion client not initialized. Check your .env file.")
        return

    try:
        topic = client.fetch_next_article()
        if topic:
            print(f"SUCCESS: Fetched next article!")
            print(f"URL: {topic.url}")
            print(f"Type: {topic.type}")
            print(f"Tags: {topic.tags}")
        else:
            print("SUCCESS: Connection worked, but no 'Pending' articles found in the database.")
            
        # Also try to list database properties to be sure
        db = client.client.databases.retrieve(database_id=client.db_id)
        print(f"Database Title: {db.get('title', [{}])[0].get('plain_text', 'Unknown')}")
        
    except Exception as e:
        print(f"FAILED: Error during connection test: {e}")

if __name__ == "__main__":
    load_dotenv(dotenv_path="generator/.env")
    test_notion()
