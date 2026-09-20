from notion_client import Client
import os
from dotenv import load_dotenv

def check_help_datasource():
    load_dotenv(dotenv_path="generator/.env")
    token = os.getenv("NOTION_TOKEN")
    client = Client(auth=token)
    print("Help for client.data_sources.query:")
    help(client.data_sources.query)

if __name__ == "__main__":
    check_help_datasource()
