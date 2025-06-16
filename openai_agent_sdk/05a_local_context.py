from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool, RunContextWrapper
from dataclasses import dataclass

from dotenv import load_dotenv
from os import getenv

load_dotenv()

gemini_api_key=getenv('GEMINI_API_KEY')


client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/'

)

@dataclass
class UserInfo:
    userName:str
    uid:str
    email:str

@function_tool
async def get_current_weather(user:RunContextWrapper[UserInfo],location:str) -> str:
    """
    get current weather for given location
    """
    print("local context: ",user.context)
    return f"the today weather in {location} city with temperature 25C"


agent = Agent(
    name="Weather AI Assistance",
    instructions="You are expert of weather information.",
    model=OpenAIChatCompletionsModel(model="gemini-1.5-flash",openai_client=client),   
    tools=[get_current_weather]
)



query = input("Enter the question: ")

user_info = UserInfo(
    userName="umar",
    uid="12345",
    email="umar@gmail.com"
)

result = Runner.run_sync(
    agent,
    query,
    context=user_info
)



print(result.final_output)

