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
async def fetch_weather(location) -> str:

    """
    Goal:
        Tell the weather for a given location.

    Args:
        location: The location to fetch the weather for.
    
    Expected Output:
        A string describe weather in given location.
    """

    print(f"Fetch Weather: {location}")
    return "sunny"


@function_tool
async def fetch_stock_price(location) -> str:
    """
    Goal:
        Fetch the stock price for a given location.

    Args:
        location (str): The location to fetch the stock price for.

    Returns:
        str: The stock price for the given location as a string.
    """
    print(f"Fetch stock: {location}")
    return "USD 0.05"


@function_tool
async def bill_calculator(unit):
    """
    Goal:
        Calculate bill base on consume unit
    Args: 
        unit : Then number of consume unit
    Return:
        Calculate bill amount
    """
    print(f'the number of consume unit: {unit}')
    rate_per_unit = 2
    amount = unit * rate_per_unit
    return amount

agent = Agent(
    name="AI Assistance",
    instructions="You are agent ai",
    model=OpenAIChatCompletionsModel(model="gemini-1.5-flash",openai_client=client),
    tools=[fetch_weather,fetch_stock_price, bill_calculator]
)



query = input("Enter the question: ")

result = Runner.run_sync(
    agent,
    query
)



print(result.final_output)

