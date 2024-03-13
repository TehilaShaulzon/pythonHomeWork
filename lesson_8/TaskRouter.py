import uvicorn

from fastapi import FastAPI, Depends, APIRouter
from fastapi import  HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, constr, ValidationError, validator, field_validator

Task_Router = APIRouter()

class Task(BaseModel):
    name: str
    description: str
    id: int
    status: bool

    # @field_validator('id')
    # def check_id(cls, id):
    #     task = [t for t in tasks if t["id"] == id]
    #     if  task==None:
    #         raise ValueError('error')
    #     return id
    #
    # @field_validator('name')
    # def check_name(cls, id):
    #     task = [t for t in tasks if t["id"] == id]
    #     if len(task["name"]) == 0:
    #         raise ValueError('error')
    #     return id

tasks = [{"name":"homeWork","description":"ertu","id":1,"status":False}]

def check_id(id: int):
    flag=False
    for i in tasks:
        if i["id"]==id:
            flag=True
    if flag:
     return id
    return -1

def check_task(new: Task):
    flag=True
    print(new)

    for i in tasks:
        if i["id"]==new.name:
            flag=False
    if flag:
         return new
    return -1

@Task_Router.get("/{id}")
async def get_task(id:int=Depends(check_id)):
    task = [t for t in tasks if t["id"] == id]
    return task


@Task_Router.post("/task/")
async def add_task(task: Task=Depends(check_task)):
    try:
        tasks.append(task.dict())
    except ValidationError:
        raise HTTPException(status_code=400, detail="oops... an error occurred")
    return f"Hello {task.name}"


@Task_Router.put("/{id}", response_model=Task)
async def update_task(newTask: Task,id:int):
    try:
        updated=jsonable_encoder(newTask)
        task = [t for t in tasks if t["id"] == id]
        task= updated
    except ValidationError:
        raise HTTPException(status_code=400, detail="oops... an error occurred")
    return updated

@Task_Router.delete("/{id}")
async def delete_task(id:int):
    try:
        task = [t for t in tasks if t["id"] == id]
        deleted=task
        del task
    except ValidationError:
        raise HTTPException(status_code=400, detail="oops... an error occurred")
    return deleted

