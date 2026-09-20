from notion_client import Client
import os, glob, re, json

client = Client(auth=os.getenv('NOTION_TOKEN'))
res = client.search(filter={'property': 'object', 'value': 'page'})
results = res.get('results', [])

md_files = glob.glob('blog/src/data/blog/*.md')
md_data = {}
for mf in md_files:
    slug = os.path.basename(mf).replace('.md', '')
    with open(mf, 'r', encoding='utf-8') as f:
        content = f.read()
    title_match = re.search(r'title:\s*["\x27]?(.*?)["\x27]?\s*\n', content)
    desc_match = re.search(r'description:\s*["\x27]?(.*?)["\x27]?\s*\n', content)
    title = title_match.group(1) if title_match else ''
    desc = desc_match.group(1) if desc_match else ''
    md_data[slug] = {
        'path': mf,
        'title': title,
        'desc': desc,
        'slug': slug
    }

to_process = []
for r in results:
    props = r.get('properties', {})
    name_list = props.get('Name', {}).get('title', [])
    title = name_list[0].get('plain_text', '').strip() if name_list else ''
    
    fb_list = props.get('facebook-post', {}).get('rich_text', [])
    fb_text = ''.join([t.get('plain_text', '') for t in fb_list]).strip()
    
    source_url = props.get('URL מקור', {}).get('url', '') or ''
    post_url = props.get('לינק לפוסט', {}).get('url', '') or ''
    status_obj = props.get('Status', {}).get('status', {})
    status = status_obj.get('name', '') if status_obj else ''
    
    final_post_list = props.get('הפוסט הסופי', {}).get('rich_text', [])
    final_post_text = ''.join([t.get('plain_text', '') for t in final_post_list]).strip()
    
    if not fb_text and (title or post_url or (source_url and 'eatwell' not in source_url) or final_post_text):
        to_process.append({
            'id': r['id'],
            'title': title,
            'status': status,
            'source_url': source_url,
            'post_url': post_url,
            'has_final_post': bool(final_post_text)
        })

print(f"Total Notion rows needing FB post: {len(to_process)}")
print(json.dumps(to_process, indent=2, ensure_ascii=False))
