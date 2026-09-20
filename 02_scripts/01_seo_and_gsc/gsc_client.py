import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/webmasters',
    'https://www.googleapis.com/auth/webmasters.readonly'
]

# Look for credentials in config directory first, then root fallback
POSSIBLE_CREDS = [
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '06_config_and_credentials', 'gsc-credentials.json')),
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'gsc-credentials.json')),
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'gsc-credentials.json')),
]
CREDENTIALS_PATH = next((p for p in POSSIBLE_CREDS if os.path.exists(p)), POSSIBLE_CREDS[0])
DEFAULT_SITE_URL = 'https://ai-world-blog.vercel.app/'

def get_service():
    if not os.path.exists(CREDENTIALS_PATH):
        print(f"Error: Credentials file not found at {CREDENTIALS_PATH}")
        sys.exit(1)
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_PATH, scopes=SCOPES
    )
    service = build('searchconsole', 'v1', credentials=creds)
    webmasters_service = build('webmasters', 'v3', credentials=creds)
    return service, webmasters_service

def list_sites():
    _, webmasters_service = get_service()
    sites = webmasters_service.sites().list().execute()
    entries = sites.get('siteEntry', [])
    print(f"\n--- Verified Sites ({len(entries)}) ---")
    for site in entries:
        print(f"- URL: {site['siteUrl']} (Permission: {site['permissionLevel']})")
    return entries

def inspect_url(inspection_url, site_url=DEFAULT_SITE_URL):
    service, _ = get_service()
    print(f"\nInspecting URL: {inspection_url} under site {site_url}...")
    request_body = {
        'inspectionUrl': inspection_url,
        'siteUrl': site_url,
        'languageCode': 'he'
    }
    try:
        response = service.urlInspection().index().inspect(body=request_body).execute()
        result = response.get('inspectionResult', {})
        index_status = result.get('indexStatusResult', {})
        print(f"\n--- Index Status for: {inspection_url} ---")
        print(f"Verdict: {index_status.get('verdict')}")
        print(f"Coverage State: {index_status.get('coverageState')}")
        print(f"Indexing State: {index_status.get('indexingState')}")
        print(f"Last Crawl Time: {index_status.get('lastCrawlTime')}")
        print(f"Robots.txt State: {index_status.get('robotsTxtState')}")
        print(f"Page Fetch State: {index_status.get('pageFetchState')}")
        print(f"Google Canonical: {index_status.get('googleCanonical')}")
        print(f"User Canonical: {index_status.get('userCanonical')}")
        return result
    except Exception as e:
        print(f"Inspection error: {e}")
        return None

def submit_sitemap(sitemap_url=None, site_url=DEFAULT_SITE_URL):
    _, webmasters_service = get_service()
    if not sitemap_url:
        sitemap_url = f"{site_url.rstrip('/')}/sitemap-index.xml"
    print(f"\nSubmitting sitemap: {sitemap_url} to site: {site_url}...")
    try:
        webmasters_service.sitemaps().submit(siteUrl=site_url, feedpath=sitemap_url).execute()
        print("Sitemap successfully submitted/refreshed!")
    except Exception as e:
        print(f"Sitemap submission error: {e}")

from datetime import datetime, timedelta, timezone

def get_analytics(days=28, limit=15, site_url=DEFAULT_SITE_URL):
    service, _ = get_service()
    end_date = datetime.now(timezone.utc) - timedelta(days=2) # GSC data has ~2-3 days lag
    start_date = end_date - timedelta(days=days)
    
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')
    
    print(f"\n--- Search Analytics ({start_str} to {end_str}) for {site_url} ---")
    request_body = {
        'startDate': start_str,
        'endDate': end_str,
        'dimensions': ['query'],
        'rowLimit': limit
    }
    try:
        response = service.searchanalytics().query(siteUrl=site_url, body=request_body).execute()
        rows = response.get('rows', [])
        if not rows:
            print("No query data available yet for this period.")
            return []
        print(f"{'Query':<40} | {'Clicks':<8} | {'Impressions':<12} | {'CTR':<8} | {'Position':<8}")
        print("-" * 85)
        for r in rows:
            q = r.get('keys', [''])[0]
            clicks = r.get('clicks', 0)
            imp = r.get('impressions', 0)
            ctr = f"{r.get('ctr', 0)*100:.1f}%"
            pos = f"{r.get('position', 0):.1f}"
            print(f"{q:<40} | {clicks:<8} | {imp:<12} | {ctr:<8} | {pos:<8}")
        return rows
    except Exception as e:
        print(f"Analytics error: {e}")
        return []

def inspect_all_posts(site_url=DEFAULT_SITE_URL):
    import glob
    blog_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'blog', 'src', 'data', 'blog'))
    files = glob.glob(os.path.join(blog_dir, '*.md'))
    
    print(f"\nFound {len(files)} blog posts. Inspecting indexing status on Google...\n")
    print(f"{'Post Slug':<55} | {'Verdict':<10} | {'Coverage State'}")
    print("-" * 105)
    
    results = []
    for f in sorted(files, reverse=True):
        basename = os.path.splitext(os.path.basename(f))[0]
        url = f"{site_url.rstrip('/')}/posts/{basename}/"
        
        service, _ = get_service()
        try:
            resp = service.urlInspection().index().inspect(body={
                'inspectionUrl': url,
                'siteUrl': site_url,
                'languageCode': 'he'
            }).execute()
            idx = resp.get('inspectionResult', {}).get('indexStatusResult', {})
            verdict = idx.get('verdict', 'UNKNOWN')
            cov = idx.get('coverageState', 'לא ידוע')
            print(f"{basename:<55} | {verdict:<10} | {cov}")
            results.append({'slug': basename, 'url': url, 'verdict': verdict, 'coverage': cov})
        except Exception as e:
            print(f"{basename:<55} | ERROR      | {e}")
    return results

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Google Search Console Management CLI')
    parser.add_argument('action', choices=['sites', 'inspect', 'inspect-all', 'sitemap', 'analytics', 'submit-post'], help='Action to perform')
    parser.add_argument('--url', help='URL to inspect or submit')
    parser.add_argument('--site', default=DEFAULT_SITE_URL, help='GSC Site property URL')
    parser.add_argument('--days', type=int, default=28, help='Days of analytics history')
    parser.add_argument('--limit', type=int, default=15, help='Max rows to return')
    
    args = parser.parse_args()
    
    if args.action == 'sites':
        list_sites()
    elif args.action == 'inspect':
        if not args.url:
            print("Error: --url is required for inspect")
            sys.exit(1)
        inspect_url(args.url, args.site)
    elif args.action == 'inspect-all':
        submit_sitemap(site_url=args.site)
        inspect_all_posts(args.site)
    elif args.action == 'sitemap':
        submit_sitemap(args.url, args.site)
    elif args.action == 'analytics':
        get_analytics(args.days, args.limit, args.site)
    elif args.action == 'submit-post':
        if not args.url:
            print("Error: --url is required for submit-post")
            sys.exit(1)
        submit_sitemap(site_url=args.site)
        inspect_url(args.url, args.site)
