from typing import Optional
from pydantic import BaseModel, EmailStr, Field, model_validator


class UserCreate(BaseModel):
    username: str = Field(..., title="Username", max_length=50)
    email: EmailStr = Field(..., title="Email", max_length=50)
    password: str = Field(..., title="Password", min_length=8, max_length=50)
    first_name: str = Field(..., title="First Name", max_length=50)
    last_name: str = Field(..., title="Last Name", max_length=50)
    is_active: bool = Field(True, title="Is Active", description="Is active")
    role: Optional[str] = Field("user", title="Role", max_length=50)
    is_superuser: bool = Field(False, title="Is superuser")
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "username": "username",
                "email": "johnwick@example.com",
                "password": "12345678",
                "first_name": "John",
                "last_name": "Wick",
                "is_active": True,
            }
        }
    }


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, title="Username", max_length=50)
    email: Optional[EmailStr] = Field(None, title="Email", max_length=50)
    password: Optional[str] = Field(None, title="Password", min_length=8, max_length=50)
    first_name: Optional[str] = Field(None, title="First Name", max_length=50)
    last_name: Optional[str] = Field(None, title="Last Name", max_length=50)
    role: Optional[str] = Field(None, title="Role", max_length=50)
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "username": "johnwick",
                "email": "johnwick@example.com",
                "password": "12345678",
                "first_name": "John",
                "last_name": "Wick",
                "role": "user"
            }
        }
    }


class UserShow(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    role: str
    model_config = {
        "from_attributes": True
    }

class ChangePasswordSchema(BaseModel):
    username: Optional[str] = Field(default=None, max_length=50)
    email: Optional[EmailStr] = Field(default=None, max_length=50)
    old_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8)

    @model_validator(mode="before")
    @classmethod
    def check_username_or_email(cls, data):
        if not data.get("username") and not data.get("email"):
            raise ValueError("Either username or email must be provided.")
        return data
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "username": "username",  # Or use "email": "johnwick@example.com"
                "old_password": "12345678",
                "new_password": "87654321"
            }
        }
    }