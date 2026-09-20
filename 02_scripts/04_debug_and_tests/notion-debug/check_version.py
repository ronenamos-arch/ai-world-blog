import notion_client
from notion_client import Client

print(f"Notion Client Version: {notion_client.__version__}")
client = Client(auth="test")
print(f"Has query: {hasattr(client.databases, 'query')}")
print(f"Methods: {[m for m in dir(client.databases) if not m.startswith('_')]}")
