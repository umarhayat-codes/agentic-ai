from typing import List
from openai import AsyncOpenAI, BaseModel
from agents import Agent, Runner, OpenAIChatCompletionsModel

from dotenv import load_dotenv
from os import getenv

load_dotenv()

gemini_api_key=getenv('GEMINI_API_KEY')


client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/'

)


class Quiz(BaseModel):
    question:str
    options: List[str]
    correct_option:str
    class Config:
        extra = "forbid"

agent = Agent(
    name="Assistant",
    instructions="You are a Quiz Agent. You generate quizes",
    model=OpenAIChatCompletionsModel(model="gemini-1.5-flash",openai_client=client),  
    output_type=Quiz
)

query = input("Enter the question: ")

result = Runner.run_sync(
    agent,
    query
)

print(result.final_output)