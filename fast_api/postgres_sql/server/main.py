from fastapi import FastAPI
from dotenv import load_dotenv

from routes import todos_route, user_routes


load_dotenv()


app = FastAPI()

app.include_router(todos_route.todos_router, prefix="/todos", tags=["Todo"])
app.include_router(user_routes.user_routes, prefix='/user', tags=["User"])


