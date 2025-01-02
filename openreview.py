import asyncio
import urllib.parse
from playwright.async_api import async_playwright

user_input = input("Enter the topic you want to search for: ")

async def main():
    search_term = urllib.parse.quote(user_input)  # Safely encode user input for the URL
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # delete headless=False if you want to run in headless mode 
        page = await browser.new_page()
        await page.goto(f'https://openreview.net/search?term={search_term}&group=all&content=all&source=forum')
        await page.wait_for_load_state("networkidle")  # Wait until the network is idle

        article_titles = page.locator("h4")
        article_count = await article_titles.count() # Get the number of articles found
        print(f"Number of articles found: {article_count}")

        for i in range(article_count):
            # Get article title text
            title = await article_titles.nth(i).text_content()
            print(f"Article #{i + 1}: {title.strip() if title else 'No title available'}")

            # Get the link of the article if available
            link_element = article_titles.nth(i).locator("a")
            link_count = await link_element.count()
            if link_count > 0:
                article_link = await link_element.first.get_attribute("href")
                print(f"Link of the article: https://openreview.net{article_link}")
            else:
                print("No link available for this article.")

        await browser.close()

asyncio.run(main())
