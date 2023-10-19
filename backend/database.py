from pymongo import MongoClient
from bson.objectid import ObjectId

from model import *
import motor.motor_asyncio
from dotenv import dotenv_values
import os

config = dotenv_values(".env")
DATABASE_URI = config.get("DATABASE_URI")
if os.getenv("DATABASE_URI"): 
    DATABASE_URI = os.getenv("DATABASE_URI") #ensures that if we have a system environment variable, it uses that instead

client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URI)

database = client.todoapp
collection = database.tasks

async def fetch_all_tasks():
    tasks = []
    cursor = collection.find({})
    async for doc in cursor:
        task = Task(**doc)
        tasks.append(task)
    return tasks

async def fetch_one_task(id):
    doc = await collection.find_one({"id": id}, {"_id": 0})
    return doc

async def create_task(task):
    doc = task.dict()
    await collection.insert_one(doc)
    result = await fetch_one_task(task.id)
    return result

async def change_task(task):
    print(task)
    id = task.id
    title = task.title
    desc = task.desc
    checked = task.checked
    await collection.update_one({"id": id}, {"$set": {"title": title, "desc": desc, "checked": checked}})
    result = await fetch_one_task(id)
    return result

async def remove_task(id):
    await collection.delete_one({"id": id})
    return True