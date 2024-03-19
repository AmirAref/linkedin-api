from fastapi import APIRouter
from src.api.endpoints import linkedin_api, first_page

api_router = APIRouter()
api_router.include_router(linkedin_api.router, tags=["linkeidn-api"])
api_router.include_router(first_page.router)
