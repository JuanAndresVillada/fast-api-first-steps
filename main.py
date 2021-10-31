#Python
from typing import Optional
from enum import Enum
#Pydantic
from pydantic import BaseModel
from pydantic import Field
#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path


app = FastAPI()

#Models

class HairColor(Enum):
    withe = "white"
    brown = "brown"
    black = "black"
    blonde = 'blonde'
    red = 'red'

class Location(BaseModel):
    city: str
    state: str
    country: str

class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        # example = "Juanito"
        ) 
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        # example = "Villadita"
        )
    age: int = Field(
        ...,
        gt=0,
        le=115
        # example = 18
        )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)
    password: str = Field(
        ...,
        min_length=1,
        )

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "first_name": "Juan Andres",
    #             "last_name": "Villada Lopez",
    #             "age": 20,
    #             "hair_color": "black",
    #             "is_married": False
    #         }   
    #     }

class PersonOut(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        # example = "Juanito"
        ) 
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        # example = "Villadita"
        )
    age: int = Field(
        ...,
        gt=0,
        le=115
        # example = 18
        )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)

@app.get('/')
def home():
    return {"Hello" : "World!"}

# Request and Response Body 

@app.post('/person/new', response_model=PersonOut)
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

# Validaciones: Request Body

@app.put('/person/{person_id}')
def update_person(
    person_id: int = Path(
        ..., 
        gt=0,
        title='Person ID', 
        description="This is the person's id. It's required and greater than 0"
    ),
    person: Person = Body(...),
    # location: Location = Body(...)
):
    # results = person.dict()
    # results.update(location.dict())

    # return results
    return person