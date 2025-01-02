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

        article_header = page.locator("div.note") # Some of the articles have a 'note' and others have 'note undefined' class
        article_count = await article_header.count() # Get the number of articles found

        print(f"Number of articles found: {article_count}")

        for i in range(article_count):
            try:
                # Get article title text
                h4_element = article_header.nth(i).locator("h4")
                h4_text = await h4_element.text_content()
                h4_text = h4_text.strip() if h4_text else "No title"
                print(f"Article #{i + 1}: {h4_text}")

                # Get the link of the article if available
                link_element = h4_element.locator("a")
                link_count = await link_element.count()
                if link_count > 0:
                    article_link = await link_element.first.get_attribute("href")
                    print(f"Link of the article: https://openreview.net{article_link}")
                else:
                    print("No link available for this article.")

                # Get the date and conference info
                li_elements = article_header.nth(i).locator("ul.note-meta-info.list-inline li")
                li_count = await li_elements.count()

                for j in range(li_count):
                    li_text = await li_elements.nth(j).text_content()
                    if "Published" in li_text:
                        print(f"Date {li_text.strip()}")
                    elif "Readers" in li_text:
                        break  # Stop processing once "Readers" is reached
                    else:
                        print(f"Conference: {li_text.strip()}")

            except Exception as e:
                print(f"Error processing article #{i + 1}: {e}")

        await browser.close()

asyncio.run(main())
