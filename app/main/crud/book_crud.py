import math
import bcrypt
from fastapi import HTTPException
from sqlalchemy import or_
import re
from typing import List, Optional, Union
import uuid
from app.main.core.i18n import __
from sqlalchemy.orm import Session
from app.main.crud.base import CRUDBase
from app.main import models,schemas


class CRUD_BOOK(CRUDBase[models.Book,schemas.BookCreate,schemas.BookUpdate]):

    @classmethod
    def get_by_uuid(cls,db: Session, uuid: str) -> Optional[models.Book]:
        return db.query(models.Book).filter(models.Book.uuid == uuid, models.Book.is_deleted==False).first()

    @classmethod
    def get_by_name(cls,db: Session, name: str) -> Optional[models.Book]:
        return db.query(models.Book).filter(models.Book.name==name, models.Book.is_deleted==False).first()

    @classmethod
    def delete(cls,db: Session, uuid: str) -> Optional[models.Book]:
        db_obj = cls.get_by_uuid(db=db, uuid=uuid)
        if not db_obj:
            raise HTTPException(status_code=404, detail=__(key="book-not-found"))
        db.delete(db_obj)
        db.commit()

    @classmethod
    def soft_delete(cls, db: Session, uuid: str) -> Optional[models.Book]:
        db_obj = cls.get_by_uuid(db=db, uuid=uuid)
        if not db_obj:
            raise HTTPException(status_code=404, detail=__(key="book-not-found"))
        db_obj.is_deleted = True
        db.commit()


    @classmethod
    def create(cls,db: Session, obj_in: schemas.BookCreate, added_by:str) -> Optional[models.Book]:
        db_obj = models.Book(
            uuid=str(uuid.uuid4()),
            name=obj_in.name,
            category_book_uuid=obj_in.category_book_uuid,
            gender=obj_in.gender,
            currency=obj_in.currency,
            price =obj_in.price,
            full_price = f"{obj_in.price} {obj_in.currency}",
            author = obj_in.author,
            year = obj_in.year,
            isbn = obj_in.isbn,
            image_uuid = obj_in.image_uuid,
            description = obj_in.description,
            publisher_date = obj_in.publisher_date,
            added_by=added_by,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


    @classmethod
    def update(cls,db: Session, obj_in: schemas.BookUpdate, added_by:str) -> Optional[models.Book]:
        db_obj = cls.get_by_uuid(db=db, uuid=obj_in.uuid)
        if not db_obj:
            raise HTTPException(status_code=404, detail=__(key="book-not-found"))
        db_obj.name = obj_in.name if obj_in.name else db_obj.name
        db_obj.gender = obj_in.gender if obj_in.gender else db_obj.gender
        db_obj.currency = obj_in.currency if obj_in.currency else db_obj.currency
        db_obj.price = obj_in.price if obj_in.price else db_obj.price
        db_obj.full_price = f"{obj_in.price} {obj_in.currency}" if not obj_in.price else f"{obj_in.price} {obj_in.currency}"
        db_obj.author = obj_in.author if obj_in.author else db_obj.author
        db_obj.year = obj_in.year if obj_in.year else db_obj.year
        db_obj.isbn = obj_in.isbn if obj_in.isbn else db_obj.isbn
        db_obj.image_uuid = obj_in.image_uuid if obj_in.image_uuid else db_obj.image_uuid
        db_obj.description = obj_in.description if obj_in.description else db_obj.description
        db_obj.publisher_date = obj_in.publisher_date if obj_in.publisher_date else db_obj.publisher_date
        db_obj.added_by = added_by if added_by else db_obj.added_by
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @classmethod
    def get_all_data(
            cls,
            *,
            db: Session,
            page: int = 1,
            per_page: int = 30,
            order: Optional[str] = None,
            order_field: Optional[str] = None,
            keyword: Optional[str] = None,

    ):
        if page < 1:
            page = 1

        record_query = db.query(models.Book).filter(models.Book.is_deleted == False)

        if keyword:
            record_query = record_query.filter(
                or_(
                    models.Book.name.ilike(f'%{keyword}%'),
                    models.Book.description.ilike(f'%{keyword}%')
                )
            )

        if order and order_field and hasattr(models.Book, order_field):
            if order == "asc":
                record_query = record_query.order_by(getattr(models.Book, order_field).asc())
            else:
                record_query = record_query.order_by(getattr(models.Book, order_field).desc())

        total = record_query.count()
        record_query = record_query.offset((page - 1) * per_page).limit(per_page).all()

        return schemas.BookResponseList(
            total=total,
            pages=math.ceil(total / per_page),
            per_page=per_page,
            current_page=page,
            data=record_query
        )



books = CRUD_BOOK(models.Book)