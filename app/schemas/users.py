from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UsersBase(BaseModel):
    username: Optional[str]=Field(title="Username",max_length=50,default=None)
    email : Optional[EmailStr] = Field(title="Email",max_length=50,default=None)
    password: Optional[str]=Field(title="Password",min_length=8,max_length=50
                                   ,default=None)
    first_name:Optional[str]=Field(title="First Name",max_length=50,default=None)
    last_name:Optional[str]=Field(title="Last Name",max_length=50,default=None)
    is_active:Optional[bool]=Field(title="Is Active",max_length=50,default=True)

    model_config = {
        "from_attributes": True
    }

class UsersAdd(UsersBase):
    username: str = Field(title="Username", max_length=50)
    email: str = Field(title="Email", max_length=50)
    password: str = Field(title="Password",min_length=8,max_length=50
                                   ,default=None)
    first_name: str = Field(title="First Name", max_length=50)
    last_name: str = Field(title="Last Name", max_length=50)
    model_config = {
        **UsersBase.model_config,
        "json_schema_extra":{
            "example":{
                "username":"username",
                "email":"johnwhich@example.com",
                "password":"12345678",
                "first_name":"John",
                "last_name":"Wick",
                "is_active":True,
            }
        }
    }
