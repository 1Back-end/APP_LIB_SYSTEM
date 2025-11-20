from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from app.main.schemas import BookSlim, AddedBy


class Return(BaseModel):
    book_uuid: str
    note: Optional[str]


class ReturnCreate(Return):
    pass


class ReturnUpdate(BaseModel):
    uuid: str
    book_uuid: str
    note: Optional[str]


class ReturnUpdateStatus(BaseModel):
    uuid: str
    status: str


class ReturnDelete(BaseModel):
    uuid: str


class ReturnResponse(BaseModel):
    uuid: str
    book: BookSlim
    customer: AddedBy
    user: AddedBy
    status: str
    date_return_exact: datetime
    notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ReturnResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page: int
    data: list[ReturnResponse]

    model_config = ConfigDict(from_attributes=True)


class ReturnSlim(BaseModel):
    book: BookSlim
    status: str
    notes: Optional[str] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)



class ReturnResponseListSlim(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page: int
    data: list[ReturnSlim]

    model_config = ConfigDict(from_attributes=True)