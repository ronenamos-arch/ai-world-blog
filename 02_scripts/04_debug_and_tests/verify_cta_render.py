import urllib.request
import re

url = "http://localhost:4322/posts/2026-04-21-gemini-api-free-google-ai-studio-guide/"
html = urllib.request.urlopen(url).read().decode("utf-8")

matches = re.findall(r'<a[^>]*href="https://google-ai-pro-drab\.vercel\.app/"[^>]*>(.*?)</a>', html, re.DOTALL)
print(f"Found {len(matches)} CTA button elements in DOM:")
for m in matches:
    print("Button text/content:", m.strip())

code_blocks = re.findall(r'<pre.*?</pre>', html, re.DOTALL)
print(f"Total <pre> code blocks on page: {len(code_blocks)}")
