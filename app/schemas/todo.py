from typing import Optional

from pydantic import BaseModel,Field
class TodoBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int]= Field(gt=0,lt=6,default=None)
    completed: Optional[bool] = False
    owner: Optional[int] = None

    model_config = {
        "from_attributes": True
    }

class TodoAddUpdate(TodoBase):
    title: str
    description: str
    priority: int = Field(gt=0,lt=6)
    completed: bool = False
    owner: int = Field(gt=0)
    model_config = {
        **TodoBase.model_config,
        "json_schema_extra": {
            "example": {
                "title": "Todos",
                "description": "Todos description",
                "priority": 5,
                "completed": False,
            }
        }
    }

class TodoUpdatePartially(TodoBase):
    model_config = {
        **TodoBase.model_config,
        "json_schema_extra": {
            "example": {
                "completed": True,
            }
        }
    }