from notion_client import Client
import os
from dotenv import load_dotenv

def check_help():
    load_dotenv(dotenv_path="generator/.env")
    token = os.getenv("NOTION_TOKEN")
    client = Client(auth=token)
    print("Help for client.databases:")
    help(client.databases)

if __name__ == "__main__":
    check_help()
