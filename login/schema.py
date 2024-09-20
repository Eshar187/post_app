from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from pydantic.types import conint
# Post info


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class UserOut(BaseModel):
    id:int
    email : EmailStr
    created_at : datetime

    class Config:
        orm_mode = True
    
class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

# we have to tell it that convert the sqlalchemy model 
# to be a pydantic model
    class Config:   
        orm_mode = True

class PostOUT(BaseModel):
    Post: Post
    votes: int
    class Config:   
        orm_mode = True
    



#Login page
#______________________________________________________________

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email : EmailStr
    password : str
    

class Token(BaseModel):
    acces_token : str 
    token_type : str 


class Tokendata(BaseModel):
    id: Optional[int] = None
    

class Vote(BaseModel):
    post_id:int
    dir:conint(le=1)
    









