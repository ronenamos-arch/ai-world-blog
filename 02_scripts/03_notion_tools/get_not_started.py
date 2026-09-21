import os
import re
from notion_client import Client

def get_token():
    candidates = [
        os.path.join(os.path.dirname(__file__), '..', '..', '06_config_and_credentials', 'env.txt'),
        os.path.join(os.path.dirname(__file__), '..', 'env.txt'),
        os.path.join(os.path.dirname(__file__), 'env.txt'),
    ]
    for env_path in candidates:
        if os.path.exists(env_path):
            with open(env_path, 'r', encoding='utf-8') as f:
                match = re.search(r'notion token\s*=\s*(\S+)', f.read(), re.I)
                if match:
                    return match.group(1).strip()
    return os.getenv('NOTION_TOKEN')

DATABASE_ID = '33d927f0e15480ed8e8ad00e60e47fbb'
token = get_token()
client = Client(auth=token)

try:
    db = client.databases.retrieve(DATABASE_ID)
    data_sources = db.get('data_sources', [])
    if data_sources:
        ds_id = data_sources[0]['id']
        results = client.data_sources.query(
            data_source_id=ds_id,
            filter={'property': 'Status', 'status': {'equals': 'Not started'}}
        ).get('results', [])
    else:
        results = []
except Exception as e:
    print(f"Direct query error: {e}, falling back to workspace search")
    all_results = client.search().get('results', [])
    results = [
        r for r in all_results
        if r.get('object') == 'page'
        and r.get('properties', {}).get('Status', {}).get('status', {}).get('name') == 'Not started'
    ]

not_started = []
for obj in results:
    props = obj.get('properties', {})
    title = 'Untitled'
    for p in props.values():
        if p.get('type') == 'title' and p.get('title'):
            title = p['title'][0]['plain_text']
            break
    url = props.get('URL מקור', {}).get('url')
    not_started.append({'id': obj['id'], 'title': title, 'url': url})

print(f'Total Not Started: {len(not_started)}')
for i, item in enumerate(not_started, 1):
    print(f"{i}. [{item['title']}] ID: {item['id']} URL: {item['url']}")