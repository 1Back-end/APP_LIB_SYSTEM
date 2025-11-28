from datetime import timedelta, datetime
from typing import Any, Optional
from fastapi import APIRouter, Depends, Body, HTTPException, Query
from sqlalchemy.orm import Session
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.config import Config
from app.main.core.dependencies import TokenRequired

router = APIRouter(prefix="/emprunts", tags=["emprunts"])

@router.post("/create",response_model=schemas.Msg)
async def create_emprunt(
    *,
    db: Session = Depends(get_db),
    obj_in : schemas.EmpruntCreate,
    current_user: models.User = Depends(TokenRequired(roles=["USER"]))
):

    book = crud.books.get_by_uuid(db=db,uuid=obj_in.book_uuid)
    if not book:
        raise HTTPException(status_code=404, detail=__(key="book-not-found"))

    crud.emprunt.create(db=db,obj_in=obj_in,added_by=current_user.uuid,user_uuid=current_user.uuid)
    return schemas.Msg(message=__(key="emprunt-created"))


@router.put("/update",response_model=schemas.Msg)
async def update_emprunt(
    *,
    db: Session = Depends(get_db),
    obj_in : schemas.EmpruntUpdate,
    current_user: models.User = Depends(TokenRequired(roles=["USER"]))
):
    book = crud.books.get_by_uuid(db=db,uuid=obj_in.book_uuid)
    if not book:
        raise HTTPException(status_code=404, detail=__(key="book-not-found"))

    crud.emprunt.update(db=db,obj_in=obj_in,added_by=current_user.uuid,user_uuid=current_user.uuid)
    return schemas.Msg(message=__(key="emprunt-updated"))


@router.put("/delete",response_model=schemas.Msg)
async def delete_emprunt(
    *,
    db: Session = Depends(get_db),
    obj_in : schemas.EmpruntDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","USER"]))
):
    crud.emprunt.delete(db=db,uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="emprunt-deleted"))


@router.put("/soft_delete",response_model=schemas.Msg)
async def soft_delete_emprunt(
    *,
    db: Session = Depends(get_db),
    obj_in : schemas.EmpruntDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","USER"]))
):
    crud.emprunt.delete(db=db,uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="emprunt-deleted"))

@router.get("/users/get_by_uuid", response_model=schemas.EmpruntResponse)
async def get_emprunt_by_uuid(
    *,
    db: Session = Depends(get_db),
    uuid : str,
   current_user : models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","USER"]))
):
    data = crud.emprunt.get_by_uuid(db=db,uuid=uuid)
    if not data:
        raise HTTPException(status_code=404, detail=__(key="emprunt-not-found"))
    return data


@router.get("/get_all_data", response_model=None)
async def get_all_emprunt(
        current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"])),
        *,
        db: Session = Depends(get_db),
        page: int = 1,
        per_page: int = 30,
        order: Optional[str] = Query(None, enum=["ASC", "DESC"]),
        order_field: Optional[str] = None,
        status: str = Query(..., enum=[st.value for st in models.EmpruntStatus]),
):
    return crud.emprunt.get_all_data(
        db=db,
        page=page,
        per_page=per_page,
        order=order,
        order_field=order_field,
        status=status,

    )

@router.get("/get_my_data", response_model=None)
async def get_my_emprunt(
        current_user: models.User = Depends(TokenRequired(roles=["USER"])),
        *,
        db: Session = Depends(get_db),
        page: int = 1,
        per_page: int = 30,
        order: Optional[str] = Query(None, enum=["ASC", "DESC"]),
        order_field: Optional[str] = None,
        status: str = Query(..., enum=[st.value for st in models.EmpruntStatus]),
):
    return crud.emprunt.get_my_emprunts(
        db=db,
        page=page,
        per_page=per_page,
        order=order,
        order_field=order_field,
        status=status,
        user_uuid=current_user.uuid,

    )