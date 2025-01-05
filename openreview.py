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
                
                # Get the authors
                authors_element = article_header.nth(i).locator("div.note-authors")
                authors_text = await authors_element.text_content()
                print(f"Authors: {authors_text.strip()}")

                # Get the date and conference info
                li_elements = article_header.nth(i).locator("ul.note-meta-info.list-inline li")
                li_count = await li_elements.count()

                if li_count > 0:
                    # Date is the first <li> element
                    date_text = await li_elements.nth(0).text_content()
                    print(f"Date", date_text.strip())
                    # Conference info is the second <li> element
                    conference_text = await li_elements.nth(1).text_content()
                    print(f"Conference: {conference_text.strip()}")

                # Open a new tab to get the abstract and keywords
                context = await browser.new_context()
                abstract_keyword_page = await context.new_page()
                await abstract_keyword_page.goto(f"https://openreview.net{article_link}")
                await abstract_keyword_page.wait_for_load_state("networkidle")

                # First condition: Check if fields exist in the first container
                fields = abstract_keyword_page.locator("div.note_contents span.note_content_field")
                if await fields.count() > 0: 
                    for j in range(await fields.count()):
                        field_text = await fields.nth(j).text_content()
                        field_text = field_text.strip() if field_text else ""
                        if "Keywords:" in field_text:
                            value_element = fields.nth(j).locator("..").locator(".note_content_value")
                            if await value_element.count() > 0:
                                keywords = await value_element.first.text_content()
                                print(f"Keywords: {keywords.strip()}")
                        if "Abstract:" in field_text:
                            value_element = fields.nth(j).locator("..").locator(".note_content_value")
                            if await value_element.count() > 0:
                                abstract = await value_element.first.text_content()
                                print(f"Abstract: {abstract.strip()}")

                # Second condition: Check other fields in the alternative structure
                other_fields = abstract_keyword_page.locator("div.note-content strong.note-content-field")
                if await other_fields.count() > 0: 
                    for j in range(await other_fields.count()):
                        field_text = await other_fields.nth(j).text_content() 
                        field_text = field_text.strip() if field_text else ""
                        if "Keywords:" in field_text:
                            value_element = other_fields.nth(j).locator("..").locator(".note-content-value")
                            if await value_element.count() > 0:
                                value_text = await value_element.first.inner_text()
                                print(f"Keywords: {value_text.strip()}")
                        if "Abstract:" in field_text:
                            value_element = other_fields.nth(j).locator("..").locator(".note-content-value")
                            if await value_element.count() > 0:
                                abstract = await value_element.first.inner_text()
                                print(f"Abstract: {abstract.strip()}")

                # Ensure to close the context when done
                await context.close()



            except Exception as e:
                print(f"Error processing article #{i + 1}: {e}")

        await browser.close()

asyncio.run(main())
