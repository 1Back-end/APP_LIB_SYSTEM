from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from app.main.schemas import AddedBy


class Category(BaseModel):
    name : str
    description : Optional[str]


class CategoryBookCreate(Category):
    pass


class CategoryBookUpdate(BaseModel):
    uuid : str
    name : Optional[str]
    description: Optional[str]


class CategoryBookDelete(BaseModel):
    uuid : str


class CategoryBookUpdateStatus(BaseModel):
    uuid : str
    is_active : bool


class CategoryBookResponse(BaseModel):
    uuid : str
    name : str
    description : Optional[str]
    is_active : bool
    user:AddedBy
    created_at: datetime
    updated_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)


class CategoryBookResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[CategoryBookResponse]

    model_config = ConfigDict(from_attributes=True)


class CategoryBookSlim(BaseModel):
    uuid: str
    name: str
    description: Optional[str]
    model_config = ConfigDict(from_attributes=True)