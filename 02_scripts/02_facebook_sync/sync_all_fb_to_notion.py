import os
from notion_client import Client
import json, time

client = Client(auth=os.getenv('NOTION_TOKEN'))

json_path = os.path.join(os.path.dirname(__file__), 'fb_posts_to_sync.json')
with open(json_path, 'r', encoding='utf-8') as f:
    posts_dict = json.load(f)

success_count = 0
for pid, data in posts_dict.items():
    fb_text = data['fb']
    title = data['title']
    try:
        props = {
            'facebook-post': {'rich_text': [{'text': {'content': fb_text}}]}
        }
        client.pages.update(page_id=pid, properties=props)
        success_count += 1
        print(f"[{success_count}/{len(posts_dict)}] Synced FB post for: {title} ({pid})")
        time.sleep(0.3)
    except Exception as e:
        print(f"Error updating {pid} ({title}): {e}")

print(f"DONE! Successfully updated {success_count}/{len(posts_dict)} Notion rows with Facebook posts.")
