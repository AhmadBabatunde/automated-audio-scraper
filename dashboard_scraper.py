from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os
import requests

load_dotenv()

def get_mp3_url(call_url, download=True):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=200)
        page = browser.new_page()

        # Step 1: Login
        page.goto("https://autoservice.digitalconcierge.io/")
        page.fill('input[name="username"]', os.getenv("DASHBOARD_USERNAME"))
        page.fill('input[name="password"]', os.getenv("DASHBOARD_PASSWORD"))
        page.click('button:enabled')
        page.wait_for_timeout(3000)

        # Step 2: Navigate to the call URL
        page.goto(call_url)
        page.wait_for_timeout(5000)

        try:
            # Wait for the first row to appear
            row_selector = 'div[row-index="0"]'
            page.wait_for_selector(row_selector, timeout=50000)
            row = page.locator(row_selector)

            # Ensure it's in view before interacting
            row.scroll_into_view_if_needed()
            page.wait_for_timeout(500)  # Allow UI to stabilize

            # Try to get bounding box and click in the center
            box = row.bounding_box()
            if box:
                center_x = box['x'] + box['width'] / 2
                center_y = box['y'] + box['height'] / 2
                page.mouse.move(center_x, center_y)
                page.mouse.click(center_x, center_y)
                print("✅ Mouse click at center of the row")
            else:
                # Fallback using JavaScript
                page.evaluate("""() => {
                    const row = document.querySelector('div[row-index="0"]');
                    if (row) {
                        row.scrollIntoView({ behavior: 'smooth', block: 'center' });
                        const event = new MouseEvent('click', { bubbles: true, cancelable: true, view: window });
                        row.dispatchEvent(event);
                    }
                }""")
                print("✅ JS-dispatched click event as fallback")

            # Step 3: Wait for the MP3 download link
            page.wait_for_selector('a#save', timeout=150000)
            print("✅ MP3 download link found.")

            mp3_url = page.query_selector('a#save').get_attribute("href")
            print("MP3 URL:", mp3_url)

            return mp3_url

        except Exception as e:
            print("Error:", e)

        finally:
            browser.close()


