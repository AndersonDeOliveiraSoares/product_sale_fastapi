from sqlalchemy.orm import Session
from app.repositories.product_repository import ProductRepository
from app.models.product import Product
from app.schemas.product import ProductCreate

class ProductController:
    def __init__(self, db: Session):
        self.repository = ProductRepository(db)

    def create_product(self, data: ProductCreate):
        new_product = Product(
            name=data.name,
            price=data.price,
            stock_quantity=data.stock_quantity,
            manufacturer_id=data.manufacturer_id
        )
        return self.repository.create(new_product)

    def list_products(self):
        products = self.repository.get_all()

        for product in products:
            if product.manufacturer:
                product.manufacturer_name = product.manufacturer.name

        return products