import asyncio
from playwright.async_api import async_playwright

user_input = input("Enter the topic you want to search for: ")
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Set headless=False to see the browser window
        page = await browser.new_page()
        await page.goto(f'https://openreview.net/search?term={user_input}&group=all&content=all&source=all')
        await page.wait_for_timeout(15000)  # Time in milliseconds (15000 ms = 15 seconds)
        await browser.close()
asyncio.run(main())