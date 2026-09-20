import urllib.request
import re
import json

url = "http://localhost:4322/posts/2026-04-14-github-for-beginners/"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(req).read().decode("utf-8")

matches = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
print(f"Total JSON-LD schemas found: {len(matches)}")
for idx, match in enumerate(matches, 1):
    try:
        data = json.loads(match)
        print(f"\n================ Schema {idx}: {data.get('@type')} ================")
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error parsing schema {idx}: {e}")
