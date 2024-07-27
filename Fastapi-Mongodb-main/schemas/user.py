from typing import List, Optional
from pydantic import BaseModel, Field

class UserBase(BaseModel):
    name: str
    email: str
    mobile_number: int
    location: str
    password: str
    role: str = Field(default="user")  # Default role is "user"

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int  

    class Config:
        from_attributes = True
