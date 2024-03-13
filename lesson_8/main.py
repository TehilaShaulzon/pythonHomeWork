import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, constr, ValidationError, validator, field_validator
from TaskRouter import Task_Router
from UsersRouter import User_Router
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(Task_Router, prefix='/Tasks', tags=["Tasks"])
app.include_router(User_Router, prefix='/Users' ,tags=["Users"])
app.mount("/static", StaticFiles(directory="static"), name="static")
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080)
