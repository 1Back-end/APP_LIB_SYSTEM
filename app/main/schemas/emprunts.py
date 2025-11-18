from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from app.main.schemas import BookSlim, AddedBy


class Emprunt(BaseModel):
    book_uuid: str
    notes: Optional[str] = None

class EmpruntCreate(Emprunt):
    pass


class EmpruntUpdate(BaseModel):
    uuid: str
    notes: Optional[str] = None
    book_uuid: str

class EmpruntUpdateStatus(BaseModel):
    uuid: str
    status: str

class EmpruntDelete(BaseModel):
    uuid: str

class EmpruntResponse(BaseModel):
    uuid: str
    book: BookSlim
    customer: AddedBy
    user: AddedBy
    status: str
    notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class EmpruntResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page: int
    data: list[EmpruntResponse]

    model_config = ConfigDict(from_attributes=True)


class EmpruntSlim(BaseModel):
    book: BookSlim
    status: str
    notes: Optional[str] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)



class EmpruntResponseListSlim(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page: int
    data: list[EmpruntSlim]

    model_config = ConfigDict(from_attributes=True)
