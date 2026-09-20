import os
from notion_client import Client
import json

client = Client(auth=os.getenv('NOTION_TOKEN'))
ds_id = '33d927f0-e154-801d-9a68-000bc771fa23'

try:
    res = client.data_sources.query(data_source_id=ds_id)
    results = res.get('results', [])
    print(f"Total results in database: {len(results)}\n")
    for i, r in enumerate(results):
        props = r.get('properties', {})
        row_info = {}
        for k, v in props.items():
            t = v.get('type')
            if t == 'title':
                val = "".join([x.get('plain_text', '') for x in v.get('title', [])])
            elif t == 'rich_text':
                val = "".join([x.get('plain_text', '') for x in v.get('rich_text', [])])
            elif t == 'status':
                val = (v.get('status') or {}).get('name')
            elif t == 'select':
                val = (v.get('select') or {}).get('name')
            elif t == 'multi_select':
                val = [x.get('name') for x in v.get('multi_select', [])]
            elif t == 'url':
                val = v.get('url')
            elif t == 'checkbox':
                val = v.get('checkbox')
            elif t == 'number':
                val = v.get('number')
            elif t == 'date':
                val = v.get('date')
            else:
                val = str(v)
            row_info[k] = val
        print(f"--- Row {i+1} [ID: {r['id']}] ---")
        for k, v in sorted(row_info.items()):
            if v is not None and v != '' and v != []:
                print(f"  {k}: {v}")
        print()

except Exception as e:
    import traceback
    traceback.print_exc()
