from pydantic import BaseModel , Field , field_validator 
import re
from datetime import datetime
from enum import Enum

class user(BaseModel):
     
    fullname : str = Field(max_length=50)
    username : str = Field(max_length=50)
    passowrd : str = Field(max_length=50)
    student : bool 
    role : str
    @field_validator("username")
    @classmethod
    def username_must_be_alphanumeric(cls, value):
        if not re.match("^[a-zA-Z0-9_]+$", value):
            raise ValueError("Username must be alphanumeric with underscores only")
        return value

class task(BaseModel):
    
    title : str = Field(max_length=50)
    description : str = Field(max_length=300)
    created_at : datetime 

class update_task(task):
    pass

    class Config :
        from_attribute = True

