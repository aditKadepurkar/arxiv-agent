from playwright.sync_api import sync_playwright

user_input = input("Enter the topic you want to search for: ")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Set headless=False to see the browser window
    page = browser.new_page()
    page.goto(f'https://openreview.net/search?term={user_input}&group=all&content=all&source=all')
    page.wait_for_timeout(15000)  # Time in milliseconds (15000 ms = 15 seconds)
    browser.close()