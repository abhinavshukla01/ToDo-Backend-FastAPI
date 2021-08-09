from models import ToDo
from fastapi import FastAPI, HTTPException, responses
from fastapi.middleware.cors import CORSMiddleware
from database import(
    fetch_all_todos,
    fetch_one_todo,
    update_todo,
    remove_todo,
    create_todo,
)

app = FastAPI()

@app.get("/")
def reat_root():
    return {"message": "Hello World"}

@app.get("/api/todo")
async def get_todo():
    response = await fetch_all_todos()
    return response

@app.get("/api/todo{title}", response_model=ToDo)
async def get_todo_by_id(title):
    response = await fetch_one_todo(title)
    if response:
        return response
    raise HTTPException(404, f"No item found with title {title}")

@app.post("/api/todo",response_model=ToDo)
async def post_todo(todo:ToDo):
    response = await create_todo(todo.dict())
    if response:
        return response
    raise HTTPException(404, "Something went Wrong")

@app.put("/api/todo{title}", response_model=ToDo)
async def put_todo(title,data):
    response = await update_todo(title,data)
    if response:
        return response
    raise HTTPException(404, f"No item found with title {title}")

@app.delete("/api/todo{title}")
async def get_todo(title):
    response = await remove_todo(title)
    if response:
        return "Item deleted successfully!"
    raise HTTPException(404, f"No item found with title {title}")



