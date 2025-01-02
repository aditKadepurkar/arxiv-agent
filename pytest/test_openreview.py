import pytest
from playwright.sync_api import Page

user_input = input("Enter the topic you want to search for: ")

def test_page_title(page: Page):
    page.goto(f'https://openreview.net/search?term={user_input}&group=all&content=all&source=forum')
    # page.wait_for_timeout(7000)  # Time in milliseconds (7 seconds)
    page.wait_for_load_state("networkidle")  # or "load" if you want to wait for everything
    assert page.title() == "Search | OpenReview"

def test_all_h4_elements(page: Page):
    page.goto(f"https://openreview.net/search?term={user_input}&group=all&content=all&source=forum")
    page.wait_for_load_state("networkidle")

    h4_elements = page.locator("h4")
    h4_count = h4_elements.count()
    print(f"Number of <h4> elements: {h4_count}")

    for i in range(h4_count):
        # Extract <h4> text
        h4_text = h4_elements.nth(i).text_content()
        print(f"Article #{i + 1}: {h4_text.strip()}")
        
        # Extract the associated <a> href if present
        a_tag = h4_elements.nth(i).locator("a")  # Look for <a> inside the specific <h4>
        if a_tag.count() > 0:
            href = a_tag.first.get_attribute("href")  # Get the href of the first <a> inside this <h4>
            print(f"Link of the article: https://openreview.net/{href}")
