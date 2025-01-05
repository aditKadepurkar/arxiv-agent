import pytest
from playwright.sync_api import Page
from playwright.sync_api import sync_playwright
user_input = input("Enter the topic you want to search for: ")

def test_page_title(page: Page):
    page.goto(f'https://openreview.net/search?term={user_input}&group=all&content=all&source=forum')
    # page.wait_for_timeout(7000)  # Time in milliseconds (7 seconds)
    page.wait_for_load_state("networkidle")  # or "load" if you want to wait for everything
    assert page.title() == "Search | OpenReview"

# def test_title_and_link(page: Page):
#     page.goto(f"https://openreview.net/search?term={user_input}&group=all&content=all&source=forum")
#     page.wait_for_load_state("networkidle")

#     h4_elements = page.locator("h4")
#     h4_count = h4_elements.count()
#     print(f"Number of <h4> elements: {h4_count}")

#     for i in range(h4_count):
#         # Extract <h4> text
#         h4_text = h4_elements.nth(i).text_content()
#         print(f"Article #{i + 1}: {h4_text.strip()}")
        
#         # Extract the associated <a> href if present
#         a_tag = h4_elements.nth(i).locator("a")  # Look for <a> inside the specific <h4>
#         if a_tag.count() > 0:
#             href = a_tag.first.get_attribute("href")  # Get the href of the first <a> inside this <h4>
#             print(f"Link of the article: https://openreview.net/{href}")

# def test_published_date(page: Page):
#     page.goto(f"https://openreview.net/search?term={user_input}&group=all&content=all&source=forum")
#     page.wait_for_load_state("networkidle")

#     div_elements = page.locator("div.note.undefined")
#     div_count = div_elements.count()
#     print(f"Number of <div class='note undefined'> elements: {div_count}")

#     for i in range(div_count):
#         # Extract <h4> text inside the current <div>
#         h4_element = div_elements.nth(i).locator("h4")
#         h4_text = h4_element.text_content().strip() if h4_element.count() > 0 else "No title"
#         print(f"Article #{i + 1}: {h4_text}")
        
#         # Extract the associated <a> href if present
#         a_tag = h4_element.locator("a")  # Look for <a> inside the specific <h4>
#         if a_tag.count() > 0:
#             href = a_tag.first.get_attribute("href")  # Get the href of the first <a> inside this <h4>
#             print(f"Link of the article: https://openreview.net/{href}")
        
#         # Extract <li> elements inside the <ul> within the current <div>
#         li_elements = div_elements.nth(i).locator("ul.note-meta-info.list-inline li")
#         li_count = li_elements.count()  # Get the total number of <li> elements

#         # Iterate through each <li> and extract content until "Readers"
#         for j in range(li_count):
#             li_text = li_elements.nth(j).text_content().strip()  # Get text content
            
#             if "Published" in li_text:
#                 print(f"Date {li_text}")
#                 continue
            
#             # Stop extraction when "Readers:" is encountered
#             if "Readers:" in li_text:
#                 break
            
#             print(f"Conference: {li_text}")

    # Locate all <li> elements
    # li_elements = page.locator("li")
    # li_count = li_elements.count()  # Get the total number of <li> elements

    # # Iterate through each <li> and print its content
    # for i in range(li_count):
    #     li_text = li_elements.nth(i).text_content().strip()  # Get text and strip extra spaces
    #     print(f"<li> Element {i + 1}: {li_text}")



def test_abstract(page: Page):
    page.goto(f"https://openreview.net/search?term={user_input}&group=all&content=all&source=forum")
    page.wait_for_load_state("networkidle")

    div_elements = page.locator("div.note")
    div_count = div_elements.count()
    print(f"Number of <div class='note undefined'> elements: {div_count}")

    for i in range(div_count):
        # Extract <h4> text inside the current <div>
        h4_element = div_elements.nth(i).locator("h4")
        h4_text = h4_element.text_content().strip() if h4_element.count() > 0 else "No title"
        print(f"Article #{i + 1}: {h4_text}")
        
        # Extract the associated <a> href if present
        a_tag = h4_element.locator("a")  # Look for <a> inside the specific <h4>
        if a_tag.count() > 0:
            href = a_tag.first.get_attribute("href")  # Get the href of the first <a> inside this <h4>
            article_link = f"https://openreview.net{href}"
            print(f"Link of the article: {article_link}")


            # print the title
            abstract_page = page.context.new_page()
            abstract_page.goto(article_link)
            abstract_page.wait_for_load_state("networkidle")

            print("bu title")
            print(abstract_page.title())


            fields = abstract_page.locator("div.note_contents span.note_content_field")
            for j in range(fields.count()):
                field_text = fields.nth(j).text_content().strip()
                if "Keywords:" in field_text:
                    value_element = fields.nth(j).locator("..").locator(".note_content_value")
                    if value_element.count() > 0:
                        value_text = value_element.first.inner_text().strip()
                        print(f"Keywords: {value_text}")
                if "Abstract:" in field_text:
                    value_element = fields.nth(j).locator("..").locator(".note_content_value")
                    if value_element.count() > 0:
                        value_text = value_element.first.inner_text().strip()
                        print(f"Abstract: {value_text}")

            other_fields = abstract_page.locator("div.note-content strong.note-content-field")
            for j in range(other_fields.count()):
                field_text = other_fields.nth(j).text_content().strip()
                if "Keywords:" in field_text:
                    value_element = other_fields.nth(j).locator("..").locator(".note-content-value")
                    if value_element.count() > 0:
                        value_text = value_element.first.inner_text().strip()
                        print(f"Keywords: {value_text}")
                if "Abstract:" in field_text:
                    value_element = other_fields.nth(j).locator("..").locator(".note-content-value")
                    if value_element.count() > 0:
                        value_text = value_element.first.inner_text().strip()
                        print(f"Abstract: {value_text}")
            # print(f'Number of fields: {fields.count()}+{other_fields.count()}')