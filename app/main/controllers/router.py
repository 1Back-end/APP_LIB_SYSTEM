from fastapi import APIRouter
from .migration_controller import router as migration
from .authentification_controller import router as authentication
from .user_controller import router as user
from .storage_controller import router as storage
from .address_controller import router as address
from .category_book_controller import router as category_book
from .book_controller import router as book
from .emprunt_controller import router as emprunt
from .retours_controller import router as retours
from .country_with_city_controller import router as country_with_city
from .bibliotheque_controller import router as bibliotheque


api_router = APIRouter()

api_router.include_router(migration)
api_router.include_router(authentication)
api_router.include_router(user)
api_router.include_router(storage)
api_router.include_router(address)
api_router.include_router(category_book)
api_router.include_router(book)
api_router.include_router(emprunt)
api_router.include_router(retours)
api_router.include_router(country_with_city)
api_router.include_router(bibliotheque)