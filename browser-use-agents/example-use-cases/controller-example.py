import asyncio
from browser_use import Browser, Controller, ActionResult
from langchain_openai import ChatOpenAI
from browser_use import Agent

from dotenv import load_dotenv
load_dotenv("../.env")

controller = Controller()
@controller.action('Open website')
async def open_website(url: str, browser: Browser=Browser()):
    page = await browser.get_current_page()
    await page.goto(url)
    return ActionResult(extracted_content='Website opened')

llm = ChatOpenAI(model="gpt-4o")

async def main():
    task = "Open the website https://www.linkedin.com and prompt the user to login"
    agent = Agent(
        task=task,
        llm=llm,
        controller=controller
    )
    await agent.run()

asyncio.run(main())