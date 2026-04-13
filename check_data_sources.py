from notion_client import Client
import os
from dotenv import load_dotenv

def check_data_sources():
    load_dotenv(dotenv_path="generator/.env")
    token = os.getenv("NOTION_TOKEN")
    client = Client(auth=token)
    print(f"Has data_sources attribute: {hasattr(client, 'data_sources')}")
    if hasattr(client, 'data_sources'):
        print(f"Methods on data_sources: {dir(client.data_sources)}")
    else:
        print("data_sources attribute missing from client.")

if __name__ == "__main__":
    check_data_sources()
