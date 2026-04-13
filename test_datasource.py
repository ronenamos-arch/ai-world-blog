import sys
import os
from dotenv import load_dotenv
from notion_client import Client

# Add generator/src to path
sys.path.append(os.path.join(os.getcwd(), 'generator'))

def test_data_source():
    load_dotenv(dotenv_path="generator/.env")
    token = os.getenv("NOTION_TOKEN")
    db_id = os.getenv("NOTION_DATABASE_ID")
    client = Client(auth=token)
    
    print(f"Testing data_sources.query on ID: {db_id}")
    try:
        response = client.data_sources.query(
            data_source_id=db_id, # Note the param name change!
            filter={
                "property": "Status",
                "status": {
                    "equals": "Pending"
                }
            },
            page_size=1
        )
        results = response.get("results", [])
        print(f"SUCCESS! Found {len(results)} pending articles.")
        for page in results:
            print(f"- {page.get('properties', {}).get('URL', {}).get('url')}")
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    test_data_source()
