from datetime import timedelta, datetime
from typing import Any, Optional
from fastapi import APIRouter, Depends, Body, HTTPException, Query
from sqlalchemy.orm import Session
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.config import Config
from app.main.core.dependencies import TokenRequired

router = APIRouter(prefix="/books", tags=["books"])

@router.post("/create",response_model=schemas.Msg)
async def create_book(
    *,
    db: Session = Depends(get_db),
    obj_in : schemas.BookCreate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    exist_name = crud.books.get_by_name(db=db,name=obj_in.name)
    if exist_name:
        raise HTTPException(status_code=409, detail=__(key="name-already-exists"))
    category = crud.category_books.get_by_uuid(db=db,uuid=obj_in.category_book_uuid)
    if not category:
        raise HTTPException(status_code=404, detail=__(key="category-book-not-found"))
    crud.books.create(db=db,obj_in=obj_in,added_by=current_user.uuid)
    return schemas.Msg(message=__(key="book-created"))


@router.put("/update",response_model=schemas.Msg)
async def update_book(
    *,
    db: Session = Depends(get_db),
    obj_in : schemas.BookUpdate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    exist_name = crud.books.get_by_name(db=db,name=obj_in.name)
    if exist_name:
        raise HTTPException(status_code=409, detail=__(key="name-already-exists"))
    category = crud.category_books.get_by_uuid(db=db,uuid=obj_in.category_book_uuid)
    if not category:
        raise HTTPException(status_code=404, detail=__(key="category-book-not-found"))
    crud.books.update(db=db,obj_in=obj_in,added_by=current_user.uuid)
    return schemas.Msg(message=__(key="book-updated"))


@router.put("/delete",response_model=schemas.Msg)
async def delete_book(
    *,
    db: Session = Depends(get_db),
    obj_in : schemas.BookDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    crud.books.delete(db=db,uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="book-deleted"))


@router.put("/soft_delete",response_model=schemas.Msg)
async def soft_delete_book(
    *,
    db: Session = Depends(get_db),
    obj_in : schemas.BookDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    crud.books.soft_delete(db=db,uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="book-deleted"))


@router.get("/get_by_uuid",response_model=schemas.BookResponse)
async def get_book_by_uuid(
        *,
        db: Session = Depends(get_db),
        uuid: str,
        current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    data = crud.books.get_by_uuid(db=db,uuid=uuid)
    if not data:
        raise HTTPException(status_code=404, detail=__(key="uuid-not-found"))
    return data


@router.get("/get_all_data", response_model=None)
async def get_all_books(
        *,
        db: Session = Depends(get_db),
        page: int = 1,
        per_page: int = 30,
        order: Optional[str] = Query(None, enum=["ASC", "DESC"]),
        order_field: Optional[str] = None,
):
    return crud.books.get_all_data(
        db=db,
        page=page,
        per_page=per_page,
        order=order,
        order_field=order_field,

    )