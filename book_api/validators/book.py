from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel, validator


class GetBook(BaseModel):
    id: int
    title: str
    number_of_pages: int
    author: str
    quantity: int
    published: Optional[datetime] = None

    @validator('published')
    def format_date(cls, v):
        return str(v+timedelta(hours=7))


class CreateBook(BaseModel):
    title: str
    number_of_pages: int
    author: str
    quantity: int


class UpdateBook(BaseModel):
    id: int
    title: str
    number_of_pages: int
    author: str
    quantity: int


class DeleteBook(BaseModel):
    id: int
