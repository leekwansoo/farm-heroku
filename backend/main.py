from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from database import *


origins = ["*"] 
# This will eventually be changed to only the origins you will use once it's deployed, to secure the app a bit more.

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get('/')
def get_root():
    return {"Ping": "Pong"}

@app.get("/api/get-task/{id}", response_model=Task)
async def get_one_task(id):
    task = await fetch_one_task(id)
    if not task: raise HTTPException(404)
    return task

@app.get("/api/get-task")
async def get_tasks():
    tasks = await fetch_all_tasks()
    if not tasks: raise HTTPException(404)
    return tasks

@app.post("/api/add-task", response_model=Task)
async def add_task(task: Task):
    result = await create_task(task)
    if not result: raise HTTPException(400)
    return result

@app.put("/api/update-task/{id}", response_model=Task)
async def update_task(task: Task):
    result = await change_task(task)
    if not result: raise HTTPException(400)
    return result

@app.delete("/api/delete-task/{id}")
async def delete_task(id):
    result = await remove_task(id)
    if not result: raise HTTPException(400)
    return result

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True) 
    
