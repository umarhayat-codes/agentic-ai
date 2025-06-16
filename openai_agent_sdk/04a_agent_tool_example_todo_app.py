import json
from typing import Dict
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
async def add_todo(title: str,description: str="",due_date:str="" ) -> Dict:
    """
    Goal: Add new todo to todos.json file
    Args: 
        title: The title of todo
        description: Optional description of todo
        due_date: Optional due date of todo in YYYY-MM-DD format
    Return:
        newly todo create of title
    """
    print(f"Add todo of title: {title}")
    with open('todos.json','r') as file:
        todos=json.load(file)
    new_todo = {
        "id":len(todos)+1,
        "title":title,
        "description":description,
        "due_date":due_date,
        "completed":False
    }   
    todos.append(new_todo)
    with open('todos.json','w') as file:
        json.dump(todos,file,indent=2)
    return new_todo


agent = Agent(
    name="Todo Assistance",
    instructions="You are expert of todo. You can add, delete, update, read the todo",
    model=OpenAIChatCompletionsModel(model="gemini-1.5-flash",openai_client=client),
    tools=[add_todo]
)



query = input("Enter the question: ")

result = Runner.run_sync(
    agent,
    query
)



print(result.final_output)

