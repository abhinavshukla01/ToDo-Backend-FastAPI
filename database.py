import os
from typing import AnyStr, Collection
from fastapi.applications import FastAPI
from models import ToDo

# MongoDB Driver
# import pymongo
import motor.motor_asyncio

# client = pymongo.MongoClient("mongodb://localhost:27017/")
db_url = os.environ.get("DB_URL", 'mongodb://localhost:27017')
print(db_url)
client = motor.motor_asyncio.AsyncIOMotorClient(db_url)
database = client["TodoList"]
Collection = database["todo"]


async def fetch_one_todo(title):
    document = await Collection.find_one({"title":title})
    return document


async def fetch_all_todos():
    todos = []
    cursor = Collection.find()
    async for document in cursor:
        todos.append(ToDo(**document))
    return todos

async def create_todo(todo):
    document = todo
    result = await Collection.insert_one(document)
    return document

async def update_todo(title, desc):
    Collection.update_one({"title":title},{"$set":{
        "description": desc
    }})
    document = await Collection.find_one({"title":title})
    return document

async def remove_todo(title):
    document = await Collection.find_one({"title":title})
    if document:
        await Collection.delete_one({"title":title})
        return True
    return False

