from fastapi import Depends
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel,function_tool

from dotenv import load_dotenv
from os import getenv


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


load_dotenv()


DATABASE_URL = 'postgresql://neondb_owner:npg_SEOwjF3qIcm7@ep-noisy-sun-a8wdxkvn-pooler.eastus2.azure.neon.tech/neondb?sslmode=require'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

print(DATABASE_URL)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()





Base = declarative_base()

class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    # completed = Column(Boolean, default=False)
    description = Column(String, nullable=True)



gemini_api_key=getenv('GEMINI_API_KEY')


client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/'

)


@function_tool
async def create_todo(title:str,description:str=""):
    """
    create new todo in postgres sql
    Args:
        title: title of todo
        description: Optional description of todo
    Return: add todo item title
    """
    db=next(get_db())
    try:
    
        db_todo = Todo(title=title,description=description)
        db.add(db_todo)
        print(f"Create todo... {db_todo.title}")
        db.commit()
        db.refresh(db_todo)
        return {
            "data":db_todo,
            "status":"success"
        } 
    except Exception as e:
        print(f"Error Create Todo.. {e}")
        return {
            "data":[],
            "status":"error",
            "message":str(e)
        } 
    

@function_tool
async def get_todo():
    """
    Fetch all todo from postgres database
    Return: list of todo
    """
    db=next(get_db())
    try:
        todos = db.query(Todo).all()
        if not todos:
            return {
                "data":[],
                "message":"Todo is not found"
            }
        
        todo_list=[]
        for todo in todos:
            todo_list.append(
                {
                    "id":todo.id,
                    "title":todo.title,
                    "description":todo.description
                }
            )
        print(f"fetch todo... {todo_list}")
        return {
            "data":todo_list,
            "status":"success"
        }
    except Exception as e:
        return {
            "data": [],
            "status":"error",
            "message":str(e)
        }

@function_tool
async def update_todo(id:int,title:str=None,description:str=None):
    """
    update todo from postgres database
    Args: 
        id: id of todo for update todo
        title: Optional title of todo 
        description: Optional description of todo 
    Return: update todo item of id
    """
    db=next(get_db())
    print(f"database... {db}")
    try:
        todo = db.query(Todo).filter(Todo.id == id).first()
        print(f"Finding todo... {todo.id}")
        if not todo:
            return {
                "data":[],
                "message":"Todo is not found"
            }
        if title:
            todo.title = title
        if description:
            todo.description = description
        print(f"Update todo... {todo.title}")
        db.commit()
        db.refresh(todo)
        return todo
    except Exception as e:
        print(f"Error update todo... {e}")
        return {
            "data": [],
            "status":"error",
            "message":str(e)
        }
    

  

@function_tool
async def delete_todo(id:int):
    """
    delete todo from postgres database
    Args: 
        id: id of todo for delete todo
    Return: delete todo item of id
    """
    db=next(get_db())
    print(f"database... {db}")
    try:
        todo = db.query(Todo).filter(Todo.id == id).first()
        print(f"Finding todo... {todo.id}")
        if not todo:
            return {
                "data":[],
                "message":"Todo is not found"
            }
        db.delete(todo)
        db.commit()
        return {"message":"Todo Deleted"}
    except Exception as e:
        print(f"Error delete todo... {e}")
        return {
            "data": [],
            "status":"error",
            "message":str(e)
        }
    



agent = Agent(
    name="ToDo Manager",
    instructions=(
        "You are a smart ToDo management assistant. "
        "You can interact with a Postgres SQL database to add new tasks, read existing tasks, "
        "update task status or content, and remove tasks based on user input. "
        "Handle each operation accurately and provide clear responses. "
        "Ensure all Postgres SQL operations are performed safely and efficiently."
    ),
    model=OpenAIChatCompletionsModel(model="gemini-1.5-flash",openai_client=client),
    tools=[create_todo,get_todo,update_todo,delete_todo]  
)



query = input("Enter the question: ")

result = Runner.run_sync(
    agent,
    query
)


print(result.final_output)
  