from datetime import timedelta, datetime
from typing import Any, Optional
from fastapi import APIRouter, Depends, Body, HTTPException, Query
from sqlalchemy.orm import Session
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.config import Config
from app.main.core.dependencies import TokenRequired

router = APIRouter(prefix="/retours", tags=["retours"])


@router.post("/create",response_model=schemas.Msg)
async def retours_create(
    *,
    db: Session = Depends(get_db),
    obj_in : schemas.ReturnCreate,
    current_user: models.User = Depends(TokenRequired(roles=["USER"]))
):
    book = crud.books.get_by_uuid(db=db,uuid=obj_in.book_uuid)
    if not book:
        raise HTTPException(status_code=404, detail=__(Key="book-not-found"))
    crud.retours.create(db=db,obj_in=obj_in,added_by=current_user.uuid,user_uuid=current_user.uuid)
    return schemas.Msg(message=__(key="retours-created"))


@router.put("/update",response_model=schemas.Msg)
async def retours_update(
    *,
    db: Session = Depends(get_db),
    obj_in : schemas.ReturnUpdate,
    current_user: models.User = Depends(TokenRequired(roles=["USER"]))
):
    book = crud.books.get_by_uuid(db=db,uuid=obj_in.book_uuid)
    if not book:
        raise HTTPException(status_code=404, detail=__(key="book-not"))
    crud.retours.update(db=db,obj_in=obj_in,added_by=current_user.uuid,user_uuid=current_user.uuid)
    return schemas.Msg(message=__("retours-update"))


@router.put("/delete",response_model=schemas.Msg)
async def retours_delete(
    *,
    db: Session = Depends(get_db),
    obj_in : schemas.ReturnDelete,
    current_user: models.User = Depends(TokenRequired(roles=["USER"]))
):
    crud.retours.delete(db=db,uuid=obj_in.uuid)
    return schemas.Msg(message=__(Key="retour-deleted"))


@router.put("/soft_delete",response_model=schemas.Msg)
async def retours_soft_delete(
    *,
    db: Session = Depends(get_db),
    obj_in : schemas.ReturnCreate,
    current_user: models.User = Depends(TokenRequired(roles=["USER"]))
):
    crud.retours.delete(db=db,uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="retours-delete"))


@router.get("/get_all_data", response_model=None)
async def get_all_retours(
        current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"])),
        *,
        db: Session = Depends(get_db),
        page: int = 1,
        per_page: int = 30,
        order: Optional[str] = Query(None, enum=["ASC", "DESC"]),
        order_field: Optional[str] = None,
):
    return crud.retours.get_all_data(
        db=db,
        page=page,
        per_page=per_page,
        order=order,
        order_field=order_field,
    )

@router.get("/get_my_data", response_model=None)
async def get_my_retours(
        current_user: models.User = Depends(TokenRequired(roles=["USER"])),
        *,
        db: Session = Depends(get_db),
        page: int = 1,
        per_page: int = 30,
        order: Optional[str] = Query(None, enum=["ASC", "DESC"]),
        order_field: Optional[str] = None,
):
    return crud.emprunt.get_my_retours(
        db=db,
        page=page,
        per_page=per_page,
        order=order,
        order_field=order_field,
        user_uuid=current_user.uuid,

    )