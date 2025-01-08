

from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str


class TodoItem(BaseModel):
    title: str
    description: Optional[str] = None
    status: str
    due_date: datetime
    owner: str
     
class Todo(BaseModel):
    title: str
    description: Optional[str] = None
    status: str
    due_date: datetime
    

   


class Token(BaseModel):
    access_token: str
    token_type: str


