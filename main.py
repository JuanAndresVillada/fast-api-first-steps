#Python
from typing import Optional
from enum import Enum
#Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr
#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path, Form, Header, Cookie, UploadFile, File
from fastapi import status



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

class PersonBase(BaseModel):
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

class Person(PersonBase):    
    password: str = Field(
        ...,
        min_length=8
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
    
class PersonOut(PersonBase):
    pass

class LoginOut(BaseModel):
    username: str = Field(...,max_length=20,example='Juanito2021')
    massage: str = Field(default="Login Succesfully!")

@app.get(
    path='/',
    status_code=status.HTTP_200_OK
    )
def home():
    return {"Hello" : "World!"}

# Request and Response Body 

@app.post(
    path='/person/new',
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED
    )
def create_person(person: Person = Body(...)):
    return person

# Validaciones: Query Parameters

@app.get(
    path='/person/detail',
    status_code=status.HTTP_202_ACCEPTED)
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

@app.get(
    path='/person/detail/{person_id}',
    status_code=status.HTTP_200_OK
    )
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

@app.put(
    path='/person/{person_id}',
    status_code=status.HTTP_200_OK
    )
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

# Formularios

@app.post(
    path='/login',
    response_model=LoginOut,
    status_code=status.HTTP_200_OK
)
def login(username: str = Form(...), password: str = Form(...)):
    return LoginOut(username=username) 

# Cookies and Headers Parameters

@app.post(
    path='/contact',
    status_code=status.HTTP_200_OK
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1
        ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1
        ),
    email: EmailStr = Form(...), 
    massage: str = Form(
        ...,
        min_length=20
        ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None),
):
    return user_agent

# files

@app.post(
    path="/post-image"
)
def post_image(
    image: UploadFile = File(...)
): 
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits=2)
    }