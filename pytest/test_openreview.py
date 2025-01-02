import pytest
from playwright.sync_api import Page

user_input = input("Enter the topic you want to search for: ")

def test_title(page: Page):
    # Navigate to the URL
    page.goto(f'https://openreview.net/search?term={user_input}&group=all&content=all&source=all')

    # Wait for the page to load completely
    # page.wait_for_timeout(7000)  # Time in milliseconds (7 seconds)
    page.wait_for_load_state("networkidle")  # or "load" if you want to wait for everything

    assert page.title() == "Search | OpenReview"

def test_title_article(page: Page):
    # Navigate to the URL
    page.goto(f'https://openreview.net/search?term={user_input}&group=all&content=all&source=all')

    
    # Wait for the page to load completely
    # page.wait_for_timeout(7000)  # Time in milliseconds (7 seconds)
    page.wait_for_load_state("networkidle")  # or "load" if you want to wait for everything


    # Assert that the title of the page is as expected
    assert page.inner_text('h4') == "first article title"
