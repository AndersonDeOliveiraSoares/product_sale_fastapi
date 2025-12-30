from sqlalchemy.orm import Session
from app.repositories.manufacturer_repository import ManufacturerRepository
from app.schemas.manufacturer import ManufacturerCreate

class ManufacturerController:
    def __init__(self, db: Session):
        self.repository = ManufacturerRepository(db)

    def create_manufacturer(self, manufacturer_data: ManufacturerCreate):
        return self.repository.create(
            name=manufacturer_data.name,
            contact_email=manufacturer_data.contact_email
        )

    def list_manufacturers(self):
        return self.repository.get_all()