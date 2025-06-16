from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel

from dotenv import load_dotenv
from os import getenv

load_dotenv()

gemini_api_key=getenv('GEMINI_API_KEY')


client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/'

)



agent = Agent(
    name="AI Assistance",
    instructions="You are agent ai",
    model=OpenAIChatCompletionsModel(model="gemini-1.5-flash",openai_client=client)    
)



query = input("Enter the question: ")

result = Runner.run_sync(
    agent,
    query
)



print(result.final_output)

