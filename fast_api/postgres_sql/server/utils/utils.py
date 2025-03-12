from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from datetime import datetime, timedelta
from dotenv import load_dotenv
from os import getenv
from uuid import uuid4
import jwt
from passlib.context import CryptContext

from models.todo_model import Users
from sqlalchemy.orm import Session
from config.database import get_db

load_dotenv()

SECRET_KEY = getenv('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
API_KEY = "api_key_header"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
api_key_header = APIKeyHeader(name=API_KEY,auto_error=False)
pwd_context = CryptContext(schemes=['bcrypt'],deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify_pwd(plain_pwd,hash_pwd):
    return pwd_context.verify(plain_pwd,hash_pwd)

def generate_api_key():
    random_uuid = uuid4().hex
    return random_uuid[:8]



def create_access_token(data: dict):
    try: 
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode,  SECRET_KEY , algorithm=ALGORITHM)
    except Exception as e:
        print('An exception occurred')
        print(e)
        return None
    
def verify_token(token: str=Depends(oauth2_scheme)):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) 
        if decoded_token:
            return decoded_token
        else:
            raise HTTPException(status_code=401, detail="Token not parsable")
    except Exception as e:
        print('An exception occurred')
        print(str(e))
        raise HTTPException(status_code=401, detail="Token decorded") 
    

def verify_api_key(api_key_header: str = Depends(api_key_header), db:Session=Depends(get_db)):
    try:
        if not api_key_header:
            raise HTTPException(status_code='401',detail="Enter api key")
            
        # if api_key_header == getenv('API_KEY'):

        db_api_key = db.query(Users).filter(Users.uuid_api_key == api_key_header)
        if db_api_key :
            return db_api_key
        else:
            raise HTTPException(status_code='401',detail="Invalid API Key")
    except Exception as e:
        print('An exception occurred')
        print(str(e))
        raise HTTPException(status_code=401, detail="API KEY")