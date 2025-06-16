from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel
from openai.types.responses import ResponseTextDeltaEvent

import asyncio 
from dotenv import load_dotenv
from os import getenv

load_dotenv()

gemini_api_key=getenv('GEMINI_API_KEY')


client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/'

)
async def main():
    agent = Agent(
        name="AI Assistance",
        instructions="You are ai agent",
        model=OpenAIChatCompletionsModel(model='gemini-1.5-flash',openai_client=client)
    )

    query = input("Enter the question: ")

    result = Runner.run_streamed(
        agent,
        input=query
    )

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

asyncio.run(main())

