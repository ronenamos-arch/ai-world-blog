import os
﻿from notion_client import Client

client = Client(auth=os.getenv('NOTION_TOKEN'))
res = client.search(filter={'property': 'object', 'value': 'page'})
results = res.get('results', [])

count_with_fb = 0
count_without_fb = 0

for r in results:
    props = r.get('properties', {})
    name_list = props.get('Name', {}).get('title', [])
    title = name_list[0].get('plain_text', '').strip() if name_list else ''
    
    fb_list = props.get('facebook-post', {}).get('rich_text', [])
    fb_text = ''.join([t.get('plain_text', '') for t in fb_list]).strip()
    
    if title:
        if fb_text:
            count_with_fb += 1
        else:
            count_without_fb += 1
            print(f"MISSING FB: '{title}' ({r['id']})")

print(f"Summary: {count_with_fb} posts HAVE Facebook posts, {count_without_fb} MISSING.")
