from fastapi import APIRouter

from api.business import router as business_router
from api.lenders import router as lenders_router
from api.loans import router as loans_router

api_router = APIRouter()

api_router.include_router(business_router, prefix="/businesses", tags=["Business"])
api_router.include_router(lenders_router, prefix="/lenders", tags=["Lenders"])
api_router.include_router(loans_router, prefix="/loans", tags=["Loans"])
