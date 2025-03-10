from pydantic import BaseModel


class CreateTodo(BaseModel):
    title:str
    description:str
    completed:bool
    # user_id:int
    token:str    