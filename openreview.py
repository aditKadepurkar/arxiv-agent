from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Set headless=False to see the browser window
    page = browser.new_page()
    page.goto('http://playwright.dev')
    # page.screenshot(path=f'example-{browser_type.name}.png')
    browser.close()