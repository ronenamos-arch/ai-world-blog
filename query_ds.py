from notion_client import Client
import os
from dotenv import load_dotenv

def query_ds():
    load_dotenv(dotenv_path="generator/.env")
    token = os.getenv("NOTION_TOKEN")
    ds_id = "33d927f0e154801d9a68000bc771fa23"
    client = Client(auth=token)
    
    print(f"Querying data_source: {ds_id}")
    try:
        response = client.data_sources.query(
            data_source_id=ds_id,
            page_size=1
        )
        results = response.get("results", [])
        print(f"SUCCESS! Found {len(results)} results.")
        for res in results:
            print(f"Result type: {res['object']}")
            if res['object'] == 'page':
                props = res.get('properties', {})
                print(f"Properties: {list(props.keys())}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    query_ds()
