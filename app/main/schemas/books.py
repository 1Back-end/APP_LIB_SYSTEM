from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from app.main.schemas import CategoryBookSlim, FileSlim1, AddedBy


class Book(BaseModel):
    name:str
    category_book_uuid:str
    gender : str
    currency : str
    price : str
    author : str
    year : str
    isbn : str
    image_uuid : str
    description :Optional[str]
    publisher_date:datetime


class BookCreate(Book):
    pass


class BookUpdate(BaseModel):
    uuid:str
    name: str
    category_book_uuid:Optional[str]
    gender : Optional[str]
    currency : Optional[str]
    price : Optional[str]
    author : Optional[str]
    year : Optional[str]
    isbn : Optional[str]
    image_uuid : Optional[str]
    description :Optional[str]
    publisher_date : Optional[datetime]

class BookDelete(BaseModel):
    uuid:str

class BookUpdateStatus(BaseModel):
    uuid:str
    is_active:bool

class BookResponse(BaseModel):
    uuid:str
    name: str
    category:CategoryBookSlim
    gender: str
    currency: str
    full_price : str
    price: str
    author: str
    year: str
    isbn: str
    image: FileSlim1
    description: Optional[str]
    is_active: bool
    user: AddedBy
    created_at: datetime
    updated_at: Optional[datetime]
    publisher_date: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)


class BookSlim(BaseModel):
    name: str
    category: CategoryBookSlim
    gender: str
    full_price:str
    author: str
    year: str
    isbn: str
    image: FileSlim1
    description: Optional[str]
    user: AddedBy
    publisher_date: datetime
    model_config = ConfigDict(from_attributes=True)


class BookResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page: int
    data: list[BookResponse]

    model_config = ConfigDict(from_attributes=True)
