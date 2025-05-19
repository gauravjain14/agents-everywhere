import os
import asyncio
from dotenv import load_dotenv
from browser_use import Browser, BrowserConfig
from playwright.async_api import Page

load_dotenv()

EMAIL    = os.getenv("LINKEDIN_EMAIL")
PASSWORD = os.getenv("LINKEDIN_PASSWORD")

async def login_if_needed(page: Page):
    # If we're on a login page (or see the login form), submit credentials
    if "login" in page.url or await page.is_visible("form.login__form"):
        await page.fill("input#session_key", EMAIL)
        await page.fill("input#session_password", PASSWORD)
        await page.click("button[type=submit]")
        # wait until we land on feed
        await page.wait_for_url("https://www.linkedin.com/feed/*", timeout=60000)

async def search_saved_posts(browser, search_term: str, max_results: int):
    ctx  = await browser.new_context()
    page = await ctx.new_page()
    # 1️⃣ Go to LinkedIn
    await page.goto("https://www.linkedin.com/")
    # 2️⃣ Login if not already
    await login_if_needed(page)
    await browser.close()
    return results

async def main():
    term = input("Keyword to search for: ")
    n    = int(input("How many posts to find? "))
    # 4️⃣ Launch Browser Use (headless=False to watch it)
    browser = await Browser(BrowserConfig(headless=False)).launch()
    matches = await search_saved_posts(browser, term, n)
    print(f"\nFound {len(matches)} posts:\n")
    for idx, m in enumerate(matches, 1):
        print(f"{idx}. {m['url']}\n   …{m['snippet']}\n")

if __name__ == "__main__":
    asyncio.run(main())
