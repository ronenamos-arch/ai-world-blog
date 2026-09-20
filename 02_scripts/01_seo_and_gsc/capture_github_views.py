import asyncio
from playwright.async_api import async_playwright

async def capture_views():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # 1. Desktop Dark
        page = await browser.new_page(viewport={"width": 1280, "height": 900})
        await page.goto("http://localhost:4322/posts/2026-04-14-github-for-beginners/", wait_until="networkidle")
        await page.evaluate("() => document.documentElement.setAttribute('data-theme', 'dark')")
        await page.screenshot(path="blog/public/github_desktop_dark.png", full_page=True)
        
        # 2. Desktop Light
        await page.evaluate("() => document.documentElement.setAttribute('data-theme', 'light')")
        await page.screenshot(path="blog/public/github_desktop_light.png", full_page=True)
        
        # 3. Mobile View (iPhone 14 size)
        mobile_page = await browser.new_page(viewport={"width": 390, "height": 844})
        await mobile_page.goto("http://localhost:4322/posts/2026-04-14-github-for-beginners/", wait_until="networkidle")
        await mobile_page.evaluate("() => document.documentElement.setAttribute('data-theme', 'dark')")
        await mobile_page.screenshot(path="blog/public/github_mobile_dark.png", full_page=True)
        
        await browser.close()
        print("Screenshots captured successfully!")

if __name__ == "__main__":
    asyncio.run(capture_views())
