import os
import asyncio
from dotenv import load_dotenv
from browser_use import Browser, BrowserConfig
from playwright.async_api import Page
from browser_use import Agent
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from typing import List

load_dotenv()

EMAIL    = os.getenv("LINKEDIN_EMAIL")
PASSWORD = os.getenv("LINKEDIN_PASSWORD")

class Post(BaseModel):
	post_title: str
	post_url: str
	num_comments: int
	hours_since_post: int


class Posts(BaseModel):
	posts: List[Post]

llm = ChatOpenAI(
	model='gpt-4.1',
	temperature=0.0,
    api_key=os.getenv("OPENAI_API_KEY")
)

# the model will see x_name and x_password, but never the actual values.
sensitive_data = {'x_name': f'{EMAIL}', 'x_password': f'{PASSWORD}'}
task = """

Go to linkedin.com. If the user is not logged in, use with x_name and x_password to login.

**Objective:**
Visit Linkedin.com and scan the saved posts to find the posts that are relevant to user's request.

**Steps:**
1. Go to https://www.linkedin.com/my-items/saved-posts/
2. If the user is not logged in, use with x_name and x_password to login.
3. Open a post and understand the contents of the post. Do not, strictly do not try to open or access videos, images, or any other media. Only create a summary from the text of the post.
4. Do a semantic match with the user request and decide whether the post answers the user's request.
5. If yes, record the post into the Post data structure.
6. Then go to the next post and repeat the process. Do this 2 times.

**Output:**
Return the posts in the Post data structure.

"""


agent = Agent(task=task, llm=llm, sensitive_data=sensitive_data)

async def main():
    request = input("Enter the post request - ")
    n    = int(input("How many posts to find? - "))
    history = await agent.run()
    result = history.final_result()
    
    if result:
        parsed: Posts = Posts.model_validate_json(result)

        for post in parsed.posts:
            print('\n--------------------------------')
            print(f'Title:            {post.post_title}')
            print(f'URL:              {post.post_url}')
            print(f'Comments:         {post.num_comments}')
            print(f'Hours since post: {post.hours_since_post}')
    else:
        print('No result')

if __name__ == "__main__":
    asyncio.run(main())
