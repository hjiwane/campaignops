from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional, Literal

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id:int
    email: EmailStr
    created_at: datetime

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    model_config = ConfigDict(from_attributes=True)
    # class Config:
    #     from_attributes = True

class PostOut(BaseModel):
    post: Post
    vote: int
    model_config = ConfigDict(from_attributes=True)
    # class Config:
    #     from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str        

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: Literal[0,1]
    


 