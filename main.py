#Python
from typing import Optional
from fastapi.datastructures import Default
#Pydantic
from pydantic import BaseModel
#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path


app = FastAPI()

#Models

class Person(BaseModel):
    first_name: str 
    last_name: str 
    age: int 
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

@app.get('/')
def home():
    return {"Hello" : "World!"}

# Request and Response Body 

@app.post('/person/new')
def create_person(person: Person = Body(...)):
    return person

# Validaciones: Query Parameters

@app.get('/person/detail')
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=30,
        title="Person Name",
        description="This is the person's name. It's between 1 and 30 characters"
        ),
    age: int = Query(
        ..., 
        title="Person Age",
        description="This is the person's age. It's required"
        )
):
    return {name: age}

# Validaciones: Path Parameters

@app.get('/person/detail/{person_id}')
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person ID",
        description="This is the person's id.  It's required"
        ),
):
    return {person_id: "It Exists!"}