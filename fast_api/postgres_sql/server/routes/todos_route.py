from fastapi import APIRouter, Depends


from utils.utils import verify_token
from sqlalchemy.orm import Session

from controllers.todos_controller import CreateTodo
from config.database import get_db
from models.todo_model import Todo




todos_router =  APIRouter()


@todos_router.post('/create')
async def create_todo(todo:CreateTodo,db: Session = Depends(get_db)):
    try:
        jwt_token = todo.token
        payload = verify_token(jwt_token)
        print(payload)
        id = payload.get('user_id')
        
        db_todo = Todo(title=todo.title,description=todo.description,completed=todo.completed,user_id=id)

        db.add(db_todo)
        print(db_todo)
        db.commit()
        db.refresh(db_todo)
        return {
            "data":db_todo,
            "status":"success"
        } 
    except Exception as e:
        return {
            "data":[],
            "status":"error",
            "message":str(e)
        } 
    

# Get Todo by id


@todos_router.get('/get/{todo_id}')
async def get_todo(todo_id:int, db : Session = Depends(get_db)):
    try:
        print(todo_id)
        todo = db.query(Todo).filter(Todo.id == todo_id).first()
        if not todo:
            return {
                "data":[],
                "message":"Todo is not found"
            }
        return {
            "data":todo,
            "status":"success"
        }
    except Exception as e:
        return {
            "data": [],
            "status":"error",
            "message":str(e)
        }
    

# Get All todo

@todos_router.get('/get')
async def get_todo( db : Session = Depends(get_db)):
    try:
        todos = db.query(Todo).all()
        if not todos:
            return {
                "data":[],
                "message":"Todo is not found"
            }
        return {
            "data":todos,
            "status":"success"
        }
    except Exception as e:
        return {
            "data": [],
            "status":"error",
            "message":str(e)
        }


# update todo

@todos_router.put('/update/{todo_id}')
async def get_todo(todo_id:int, update_todo:CreateTodo , db : Session = Depends(get_db)):
    try:
        todo = db.query(Todo).filter(Todo.id == todo_id).first()
        if not todo:
            return {
                "data":[],
                "message":"Todo is not found"
            }
        todo.title = update_todo.title
        todo.description = update_todo.description
        todo.completed = update_todo.completed
        db.commit()
        db.refresh(todo)
        return todo
    except Exception as e:
        return {
            "data": [],
            "status":"error",
            "message":str(e)
        }
    

# delete todo

@todos_router.delete('/delete/{todo_id}')
async def delete_todo(todo_id : int, db : Session = Depends(get_db)):
    try:
        todo = db.query(Todo).filter(Todo.id == todo_id).first()
        if not todo:
            return {
                "data":[],
                "message":"Todo is not found"
            }
        db.delete(todo)
        db.commit()
        return {"message":"Todo Deleted"}
    except Exception as e:
        return {"data":[],"status":"error","message":str(e)}