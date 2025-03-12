from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from models.todo_model import Users
from config.database import get_db
from controllers.user_controllers import UserCreate, UserLogin
from utils.utils import create_access_token, hash_password, verify_pwd


user_routes = APIRouter()

@user_routes.post('/register')
def register(user:UserCreate, db:Session=Depends(get_db)):
    hash_pwd = hash_password(user.password)
    valid_user = Users(name=user.name, email=user.email, password=hash_pwd)
    db.add(valid_user)
    db.commit()
    db.refresh(valid_user)
    db_user = db.query(Users).filter(Users.email == valid_user.email).first()
    token = create_access_token(data={"name":db_user.name,"email":db_user.email,"user_id":db_user.id})
    return {
        "data":valid_user,
        "message":"Register Successfully",
        "status":"success",
        "token":token
    }

@user_routes.post('/login')
def login(user:UserLogin, db:Session=Depends(get_db)):
    db_user = db.query(Users).filter(Users.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=400,detail="User Not Found")
    # if db_user.password != user.password:
    #     raise HTTPException(status_code=401, detail="Password not match")
    
    is_valid_password = verify_pwd(user.password,db_user.password)
    if is_valid_password == False:
        raise HTTPException(status_code='401',detail="Invalid Password")
    token = create_access_token(data={"email":db_user.email,"name":db_user.name,'user_id':db_user.id})
    user_data = {
        "name":db_user.name,
        "email":db_user.email,
        "password":db_user.password,
        "token":token
    }
    return {
        "data":user_data,
        "message":"User Login Successfully",
        "status":"success"
    }