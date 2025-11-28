from datetime import timedelta, datetime
from typing import Any, Optional
from fastapi import APIRouter, Depends, Body, HTTPException, Query
from sqlalchemy.orm import Session
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.config import Config
from app.main.core.dependencies import TokenRequired

router = APIRouter(prefix="/bibliotheques", tags=["bibliotheques"])

@router.post("/create",response_model=schemas.Msg)
async def create_bibliotheque(
    *,
    db: Session = Depends(get_db),
    obj_in : schemas.BibliothequeCreate,
):
    country = crud.country_with_city.get_country_by_uuid(db=db,uuid=obj_in.country_uuid)
    if not country:
        raise HTTPException(status_code=404, detail=__(key="country-not-found"))
    
    city = crud.contry_with_city_crud.get_city_by_uuid(db=db,uuid=obj_in.city_uuid)
    if not city:
        raise HTTPException(status_code=404, detail=__(key="city-not-found"))
    
    address = crud.address.get_by_uuid(db=db,uuid=obj_in.address_uuid)
    if not address:
        raise HTTPException(status_code=404, detail=__(key="address-not-found"))
    
    exist_email = crud.user.get_by_email(db=db,email=obj_in.email)
    if exist_email:
        raise HTTPException(status_code=409, detail=__(key="email-already-exist"))
    
    exist_phone_number = crud.user.get_by_phone_number(db=db,uuid=obj_in.phone_number)
    if exist_phone_number:
        raise HTTPException(status_code=409, detail=__(key="phone-number-already-exist"))
    
    if obj_in.phone_number_2:
        exist_phone_number_2 = crud.user.get_by_phone_number_2(db=db,uuid=obj_in.phone_number_2)
        raise HTTPException(status_code=409, detail=__(key="phone-number-already-exist"))
    
    exist_id_number = crud.bibliotheque.get_by_id_number(db=db,uuid=obj_in.id_number)
    if exist_id_number:
        raise HTTPException(status_code=409, detail=__(key="id-number-already-exist"))
    
    crud.bibliotheque.create(db=db,obj_in=obj_in)
    return schemas.Msg(message=__(key="bibliotheque-created"))


@router.put("/update",response_model=schemas.Msg)
async def update_bibliotheque(
    *,
    db: Session = Depends(get_db),
    obj_in : schemas.BibliothequeUpdate,
    current_user : models.User = Depends(TokenRequired(roles=["MANAGER","USER"]))
):
    country = crud.country_with_city.get_country_by_uuid(db=db,uuid=obj_in.country_uuid)
    if not country:
        raise HTTPException(status_code=404, detail=__(key="country-not-found"))
    
    city = crud.contry_with_city_crud.get_city_by_uuid(db=db,uuid=obj_in.city_uuid)
    if not city:
        raise HTTPException(status_code=404, detail=__(key="city-not-found"))
    
    address = crud.address.get_by_uuid(db=db,uuid=obj_in.address_uuid)
    if not address:
        raise HTTPException(status_code=404, detail=__(key="address-not-found"))
    
    crud.bibliotheque.update(db=db,obj_in=obj_in)
    return schemas.Msg(message=__(key="bibliotheque-updated"))

@router.put("/update_status",response_model=schemas.Msg)
async def bibliotheque_update_status(
    *,
    db: Session = Depends(get_db),
    obj_in : schemas.BibliothequeUpdateStatus,
):
    crud.bibliotheque.update_status(db=db,uuid=obj_in.uuid,status=obj_in.status)
    return schemas.Msg(message=__(key="bibliotheque-updated"))

@router.delete("/delete",response_model=schemas.Msg)
async def bibliotheque_delete(
    *,
    db: Session = Depends(get_db),
    obj_in : schemas.BibliothequeDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","USER"]))
):
    crud.bibliotheque.delete(db=db,uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="bibliotheque-deleted"))

@router.put("/soft_delete",response_model=schemas.Msg)
async def bibliotheque_soft_delete(
    *,
    db: Session = Depends(get_db),
    obj_in : schemas.BibliothequeDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","USER"]))
):
    crud.bibliotheque.soft_delete(db=db,uuid=obj_in.uuid)
    return schemas.Msg(message=__(key="bibliotheque-deleted"))


@router.get("/get_all_data", response_model=None)
async def get_all_bibliotheque(
        current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"])),
        *,
        db: Session = Depends(get_db),
        page: int = 1,
        per_page: int = 30,
        order: Optional[str] = Query(None, enum=["ASC", "DESC"]),
        order_field: Optional[str] = None,
        status: str = Query(..., enum=[st.value for st in models.BibliothequeStatus]),
):
    return crud.bibliotheque.get_all_data(
        db=db,
        page=page,
        per_page=per_page,
        order=order,
        order_field=order_field,
        status=status,

    )


@router.get("/get_my_data", response_model=None)
async def get_my_bibliotheque(
        current_user: models.User = Depends(TokenRequired(roles=["USER"])),
        *,
        db: Session = Depends(get_db),
        page: int = 1,
        per_page: int = 30,
        order: Optional[str] = Query(None, enum=["ASC", "DESC"]),
        order_field: Optional[str] = None,
        status: str = Query(..., enum=[st.value for st in models.EmpruntStatus]),
):
    return crud.bibliotheque.get_my_bibliothque(
        db=db,
        page=page,
        per_page=per_page,
        order=order,
        order_field=order_field,
        status=status,
        user_uuid=current_user.uuid,

    )