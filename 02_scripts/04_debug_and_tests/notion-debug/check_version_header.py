from notion_client import Client
import os
from dotenv import load_dotenv

def check_api_version():
    load_dotenv(dotenv_path="generator/.env")
    token = os.getenv("NOTION_TOKEN")
    client = Client(auth=token)
    print(f"Default Notion API Version: {client.options.version}")

if __name__ == "__main__":
    check_api_version()
