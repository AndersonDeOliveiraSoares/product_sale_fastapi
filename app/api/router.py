from fastapi import APIRouter
from .v1.endpoints import manufacturer,product,sale,customer # Certifique-se que criou esta pasta v1/endpoints

api_router = APIRouter()
api_router.include_router(
    manufacturer.router,
    prefix="/factories",
    tags=["Manufacturers"]
)

api_router.include_router(
    product.router,
    prefix="/products",
    tags=["Products"]
)

api_router.include_router(sale.router, prefix="/sales", tags=["Sales"])

api_router.include_router(customer.router, prefix="/customers", tags=["Customers"])

