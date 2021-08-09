import os
from typing import AnyStr, Collection
from fastapi.applications import FastAPI
from models import ToDo
from loguru import logger
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
    logger.debug("Fetch all todo function called")
    todos = []
    cursor = Collection.find()
    logger.debug("documents are find in cursor variable")
    async for document in cursor:
        logger.debug("Looping through cursor to get all documents all keys ")
        todos.append(ToDo(**document))
    logger.debug("returned all todos")
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

