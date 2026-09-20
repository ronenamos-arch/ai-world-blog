import os
from dotenv import load_dotenv
from notion_client import Client

def check_methods():
    load_dotenv(dotenv_path="generator/.env")
    token = os.getenv("NOTION_TOKEN")
    client = Client(auth=token)
    print(f"Databases object: {client.databases}")
    print(f"Directory of databases object: {dir(client.databases)}")
    if hasattr(client.databases, 'query'):
        print("SUCCESS: 'query' method exists!")
    else:
        print("FAILURE: 'query' method does NOT exist!")

if __name__ == "__main__":
    check_methods()
