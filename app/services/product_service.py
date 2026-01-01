"""
Camada de serviço para Produtos.
Contém toda a lógica de negócio e validações.
"""

import logging
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.product import Product
from app.models.manufacturer import Manufacturer
from app.schemas.product import ProductCreate, ProductUpdate
from app.exceptions import (
    ProductNotFoundException,
    ManufacturerNotFoundException,
    NegativeStockException,
    InvalidPriceException,
    DatabaseException,
    InsufficientStockException
)

logger = logging.getLogger(__name__)


class ProductService:
    """Serviço de gerenciamento de produtos."""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """
        Lista todos os produtos com paginação.

        Args:
            skip: Número de registros a pular
            limit: Número máximo de registros a retornar

        Returns:
            Lista de produtos

        Raises:
            DatabaseException: Se houver erro ao acessar o banco
        """
        try:
            return self.db.query(Product).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            logger.error(f"Erro ao listar produtos: {str(e)}")
            raise DatabaseException("Erro ao buscar lista de produtos.")

    def get_by_id(self, product_id: int) -> Product:
        """
        Busca produto por ID.

        Args:
            product_id: ID do produto

        Returns:
            Produto encontrado

        Raises:
            ProductNotFoundException: Se o produto não existir
            DatabaseException: Se houver erro ao acessar o banco
        """
        try:
            product = self.db.query(Product).filter(Product.id == product_id).first()
            if not product:
                raise ProductNotFoundException(product_id)
            return product
        except ProductNotFoundException:
            raise
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar produto {product_id}: {str(e)}")
            raise DatabaseException(f"Erro ao buscar produto com ID {product_id}.")

    def create(self, product_data: ProductCreate) -> Product:
        """
        Cria um novo produto.

        Args:
            product_data: Dados do produto a ser criado

        Returns:
            Produto criado

        Raises:
            ManufacturerNotFoundException: Se o fabricante não existir
            InvalidPriceException: Se o preço for inválido
            NegativeStockException: Se o estoque for negativo
            DatabaseException: Se houver erro ao salvar
        """
        try:
            # Valida se o fabricante existe
            manufacturer = self.db.query(Manufacturer).filter(
                Manufacturer.id == product_data.manufacturer_id
            ).first()

            if not manufacturer:
                raise ManufacturerNotFoundException(product_data.manufacturer_id)

            # Validações de negócio adicionais
            if product_data.price <= 0:
                raise InvalidPriceException(float(product_data.price))

            if product_data.stock_quantity < 0:
                raise NegativeStockException(product_data.name, product_data.stock_quantity)

            # Cria o produto
            new_product = Product(
                name=product_data.name,
                category=product_data.category,
                price=product_data.price,
                stock_quantity=product_data.stock_quantity,
                manufacturer_id=product_data.manufacturer_id
            )

            self.db.add(new_product)
            self.db.commit()
            self.db.refresh(new_product)

            logger.info(f"Produto criado: ID={new_product.id}, Nome={new_product.name}")
            return new_product

        except (ManufacturerNotFoundException, InvalidPriceException, NegativeStockException):
            raise
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Erro ao criar produto: {str(e)}")
            raise DatabaseException("Erro ao salvar o produto no banco de dados.")

    def update(self, product_id: int, product_data: ProductUpdate) -> Product:
        """
        Atualiza um produto existente.

        Args:
            product_id: ID do produto a ser atualizado
            product_data: Dados a serem atualizados

        Returns:
            Produto atualizado

        Raises:
            ProductNotFoundException: Se o produto não existir
            ManufacturerNotFoundException: Se o novo fabricante não existir
            DatabaseException: Se houver erro ao salvar
        """
        try:
            product = self.get_by_id(product_id)

            # Atualiza apenas os campos fornecidos
            update_data = product_data.dict(exclude_unset=True)

            # Valida fabricante se for alterado
            if 'manufacturer_id' in update_data:
                manufacturer = self.db.query(Manufacturer).filter(
                    Manufacturer.id == update_data['manufacturer_id']
                ).first()
                if not manufacturer:
                    raise ManufacturerNotFoundException(update_data['manufacturer_id'])

            # Valida preço se for alterado
            if 'price' in update_data and update_data['price'] <= 0:
                raise InvalidPriceException(float(update_data['price']))

            # Valida estoque se for alterado
            if 'stock_quantity' in update_data and update_data['stock_quantity'] < 0:
                raise NegativeStockException(product.name, update_data['stock_quantity'])

            for field, value in update_data.items():
                setattr(product, field, value)

            self.db.commit()
            self.db.refresh(product)

            logger.info(f"Produto atualizado: ID={product.id}")
            return product

        except (ProductNotFoundException, ManufacturerNotFoundException, InvalidPriceException, NegativeStockException):
            raise
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Erro ao atualizar produto {product_id}: {str(e)}")
            raise DatabaseException("Erro ao atualizar o produto.")

    def delete(self, product_id: int) -> bool:
        """
        Deleta um produto.

        Args:
            product_id: ID do produto a ser deletado

        Returns:
            True se deletado com sucesso

        Raises:
            ProductNotFoundException: Se o produto não existir
            DatabaseException: Se houver erro ao deletar
        """
        try:
            product = self.get_by_id(product_id)
            self.db.delete(product)
            self.db.commit()

            logger.info(f"Produto deletado: ID={product_id}")
            return True

        except ProductNotFoundException:
            raise
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Erro ao deletar produto {product_id}: {str(e)}")
            raise DatabaseException("Erro ao deletar o produto.")

    def decrease_stock(self, product_id: int, quantity: int) -> Product:
        """
        Diminui o estoque de um produto (usado em vendas).

        Args:
            product_id: ID do produto
            quantity: Quantidade a diminuir

        Returns:
            Produto atualizado

        Raises:
            ProductNotFoundException: Se o produto não existir
            InsufficientStockException: Se não houver estoque suficiente
            DatabaseException: Se houver erro ao salvar
        """
        try:
            product = self.get_by_id(product_id)

            if product.stock_quantity < quantity:
                raise InsufficientStockException(
                    product_name=product.name,
                    requested=quantity,
                    available=product.stock_quantity
                )

            product.stock_quantity -= quantity
            self.db.commit()
            self.db.refresh(product)

            logger.info(f"Estoque reduzido: Produto {product.name}, Qtd: -{quantity}")
            return product

        except (ProductNotFoundException, InsufficientStockException):
            raise
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Erro ao reduzir estoque do produto {product_id}: {str(e)}")
            raise DatabaseException("Erro ao atualizar o estoque.")

    def get_low_stock_products(self, threshold: int = 10) -> List[Product]:
        """
        Retorna produtos com estoque baixo.

        Args:
            threshold: Limite de estoque considerado baixo

        Returns:
            Lista de produtos com estoque baixo
        """
        try:
            return self.db.query(Product).filter(
                Product.stock_quantity <= threshold
            ).all()
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar produtos com estoque baixo: {str(e)}")
            raise DatabaseException("Erro ao buscar relatório de estoque baixo.")