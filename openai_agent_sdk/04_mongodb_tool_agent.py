from bson import ObjectId
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool

from dotenv import load_dotenv
from os import getenv


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()




uri = "mongodb+srv://agent:admin098@cluster0.5gks7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
mongo_client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    mongo_client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


gemini_api_key=getenv('GEMINI_API_KEY')


client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/'

)

@function_tool
async def create_todo(title:str, description:str=""):
    """
    Create new Todo in mongodb database
    Args: 
        title: title of todo
        description: Optional desciption of todo
    Return:
        newly todo create item title
    """
    try:
        agent_db = mongo_client['agent_db']
        todo_collection = agent_db['todo']
        new_todo={
            "title":title,
            "description":description,
            "status":"pending"
        }
        result=todo_collection.insert_one(new_todo)
        return {"id":str(result.inserted_id),**new_todo}
    except Exception as e:
        raise ValueError(f"Error Create todo: {e}")


@function_tool
async def fetch_todo():
    """
    fetch all todo from mongodb database
    Return:
        A list of todo item
    """
    try:
        agent_db = mongo_client['agent_db']
        todo_collection = agent_db['todo']
        todos=list(todo_collection.find())
        for todo in todos:
            todo['_id']=str(todo['_id'])
        print(f'fetch todo... {todos}')
        return todos
    except Exception as e:
        print(f"Error fetch todo: {e}")


@function_tool
async def update_todo(todo_id:str,title:str=None,description:str=None,status:str=None):
    """
    Update exist todo from mongodb database
    Args:
        todo_id:ID of todo for update
        title:Optional update title of todo
        description:Optional update description of todo
        status:Optional update status of todo
    Return:
        The update todo item
    """
    try:
        agent_db = mongo_client['agent_db']
        todo_collection = agent_db['todo']
        update_field={}
        if title:
            update_field['title']=title
        if description:
            update_field['description']=description
        if status:
            update_field['status']=status
        result=todo_collection.update_one({"_id":ObjectId(todo_id)},{"$set":update_field})
        if result.matched_count==0:
            raise ValueError(f"Todo not match")
        print(f"Update Todo... {update_field}")
        return {"_id":todo_id,"update":update_field}
    except Exception as e:
        print(f"Error Update todo: {e}")

@function_tool
async def delete_todo(title:str):
    """
    delete todo from mongodb database
    Args: 
        title: title of todo to delete
    Return:
        confirmation message
    """
    try:
        agent_db = mongo_client['agent_db']
        todo_collection = agent_db['todo']
        result=todo_collection.delete_one({"title":title})
        print(f"Deleted Todo... {result}")
        if result.deleted_count == 0:
            raise ValueError(f"Todo not match")
        return {"message":"todo successfully deleted"}
    except Exception as e:
        print(f"Error delete todo: {e}")

agent = Agent(
    name="ToDo Manager",
    instructions=(
        "You are a smart ToDo management assistant. "
        "You can interact with a MongoDB database to add new tasks, read existing tasks, "
        "update task status or content, and remove tasks based on user input. "
        "Handle each operation accurately and provide clear responses. "
        "Ensure all MongoDB operations are performed safely and efficiently."
    ),
    model=OpenAIChatCompletionsModel(model="gemini-1.5-flash",openai_client=client),    
    tools=[create_todo,fetch_todo,update_todo,delete_todo]
)



query = input("Enter the question: ")

result = Runner.run_sync(
    agent,
    query
)



print(result.final_output)



