from typing import Dict
from httpx import request
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool

from dotenv import load_dotenv
from os import getenv

load_dotenv()

gemini_api_key=getenv('GEMINI_API_KEY')


client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/'

)

@function_tool
async def fetch_user_info(user_name:str)->Dict:
    """
    Fetch user information from github api
    Args: user_name: the github user_name
    Return: Dictionary which contain user all information
    """
    try:
        url=f'https://api.github.com/users/{user_name}'
        response = request("Get",url)
        print("fetching data...",response.json())
        if response.status_code==200:
            return response.json()
        else:
            raise ValueError(f"Error fetch user infor",response.status_code)
    except Exception as e:
        raise ValueError(f"Error fetch user infor",e)

agent = Agent(
    name="GitHub Assistant",
    instructions=(
        "You are an expert on GitHub. Fetch all data of user from github And also fetch specific information include in github."
    ),
    model=OpenAIChatCompletionsModel(model="gemini-1.5-flash",openai_client=client),
    tools=[fetch_user_info]
)





query = input("Enter the question: ")

result = Runner.run_sync(
    agent,
    query
)



print(result.final_output)

