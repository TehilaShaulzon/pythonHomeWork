import uvicorn

from fastapi import FastAPI, Depends, APIRouter
from fastapi import  HTTPException
from fastapi.encoders import jsonable_encoder

from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, constr, ValidationError, validator, field_validator

User_Router = APIRouter()

class User(BaseModel):
    name: str
    id: int
    age: int

    # @field_validator('id')
    # def check_id(cls, id):
    #     user = [t for t in users if t["id"] == id]
    #     if  user==None:
    #         raise ValueError('error')
    #     return id
    #
    # @field_validator('name')
    # def check_name(cls, id):
    #     user = [t for t in users if t["id"] == id]
    #     if len(user["name"]) == 0:
    #         raise ValueError('error')
    #     return id


users = [{"name":"sara","id":1,"age":5}]

def check_id(id: int):
    flag=False
    for i in users:
        if i["id"]==id:
            flag=True
    if flag:
     return id
    return -1

def check_name(new: User):
    flag=True
    print(new)

    for i in users:
        if i["id"]==new.name:
            flag=False
    if flag:
         return new
    return -1

@User_Router.get("/{id}")
async def get_user(id:int=Depends(check_id)):
    user = [t for t in users if t["id"] == id]
    return user


@User_Router.post("/user/")
async def add_user(user: User=Depends(check_name)):
    try:
        users.append(user.dict())
    except ValidationError:
        raise HTTPException(status_code=400, detail="oops... an error occurred")
    return f"Hello {user.name}"


@User_Router.put("/{id}", response_model=User)
async def update_user(newUser: User,id:int):
    try:
        updated=jsonable_encoder(newUser)
        user = [t for t in users if t["id"] == id]
        user= updated
    except ValidationError:
        raise HTTPException(status_code=400, detail="oops... an error occurred")
    return updated

@User_Router.delete("/{id}")
async def delete_user(id:int):
    try:
        user = [t for t in users if t["id"] == id]
        deleted=user
        del user
    except ValidationError:
        raise HTTPException(status_code=400, detail="oops... an error occurred")
    return deleted

