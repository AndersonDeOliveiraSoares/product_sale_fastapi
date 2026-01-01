from sqlalchemy.orm import Session
from app.repositories.product_repository import ProductRepository
from app.models.product import Product
from app.schemas.product import ProductCreate
from app.exceptions import ManufacturerNotFoundException, InvalidPriceException
from app.models.manufacturer import Manufacturer


class ProductController:
    def __init__(self, db: Session):
        self.db = db
        self.repository = ProductRepository(db)

    def create_product(self, data: ProductCreate):
        manufacturer = self.db.query(Manufacturer).filter(Manufacturer.id == data.manufacturer_id).first()
        if not manufacturer:
            raise ManufacturerNotFoundException(data.manufacturer_id)

        new_product = Product(
            name=data.name,
            price=data.price,
            stock_quantity=data.stock_quantity,
            manufacturer_id=data.manufacturer_id
        )
        return self.repository.create(new_product)

    def get_product(self, product_id: int):
        """Usa o repositório para garantir retorno ou erro 404."""
        return self.repository.get_by_id_or_404(product_id)

    def list_products(self):
        products = self.repository.get_all()

        for product in products:
            if product.manufacturer:
                product.manufacturer_name = product.manufacturer.name

        return products