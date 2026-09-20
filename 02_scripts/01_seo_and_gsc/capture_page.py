import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 900})
        await page.goto("http://localhost:4322/posts/2026-04-21-gemini-api-free-google-ai-studio-guide/", wait_until="networkidle")
        await page.screenshot(path="blog/public/rendered_gemini_post.png", full_page=True)
        await browser.close()
        print("Screenshot saved to blog/public/rendered_gemini_post.png")

if __name__ == "__main__":
    asyncio.run(main())
