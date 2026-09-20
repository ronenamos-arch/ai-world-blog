import os
﻿from notion_client import Client

client = Client(auth=os.getenv('NOTION_TOKEN'))

posts = [
    {
        'id': '3dc927f0-e154-806b-b2fd-e14ea10ee568',
        'url': 'https://ai-world-blog.vercel.app/posts/2026-09-18-astra-deepseek/'
    },
    {
        'id': '3dc927f0-e154-8050-9f6a-cd81f5f6b2cc',
        'url': 'https://ai-world-blog.vercel.app/posts/2026-09-18-grok-bot-playbook/'
    }
]

for p in posts:
    props = {
        'Status': {'status': {'name': 'Published'}},
        'פורסם באתר': {'checkbox': True},
        'ביקורת אנושית': {'checkbox': True},
        'לינק לפוסט': {'url': p['url']},
        'תאריך פרסום': {'date': {'start': '2026-09-18'}}
    }
    client.pages.update(page_id=p['id'], properties=props)
    print("Published page", p['id'], "->", p['url'])

print("Both posts marked as Published in Notion!")
