import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, constr, ValidationError, validator, field_validator

app = FastAPI()


class Task(BaseModel):
    name: str
    description: str
    id: int
    status: bool

    @field_validator('id')
    def check_id(cls, id):
        task = [t for t in tasks if t["id"] == id]
        if  task==None:
            raise ValueError('error')
        return id

    @field_validator('name')
    def check_name(cls, id):
        task = [t for t in tasks if t["id"] == id]
        if len(task["name"]) == 0:
            raise ValueError('error')
        return id

tasks = [{"name":"sara","description":"ertu","id":5,"status":False}]

@app.get("/{id}")
async def get_task(id:int):
    task = [t for t in tasks if t["id"] == id]
    return task


@app.post("/task/")
async def add_task(task: Task):
    try:
        tasks.append(task.dict())
    except ValidationError:
        raise HTTPException(status_code=400, detail="oops... an error occurred")
    return f"Hello {task.name}"


@app.put("/{id}", response_model=Task)
async def update_task(newTask: Task,id:int):
    try:
        updated=jsonable_encoder(newTask)
        task = [t for t in tasks if t["id"] == id]
        task= updated
    except ValidationError:
        raise HTTPException(status_code=400, detail="oops... an error occurred")
    return updated

@app.delete("/{id}")
async def delete_task(id:int):
    try:
        task = [t for t in tasks if t["id"] == id]
        deleted=task
        del task
    except ValidationError:
        raise HTTPException(status_code=400, detail="oops... an error occurred")
    return deleted


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080)
