"""
Sistema centralizado de exceções customizadas para o ERP.
Facilita o tratamento consistente de erros em toda a aplicação.
"""

from typing import Any, Optional
from fastapi import HTTPException, status


class BaseAPIException(HTTPException):
    """Classe base para todas as exceções da API."""

    def __init__(
            self,
            status_code: int,
            detail: str,
            error_code: str,
            extra: Optional[dict[str, Any]] = None
    ):
        self.error_code = error_code
        self.extra = extra or {}
        super().__init__(
            status_code=status_code,
            detail={
                "message": detail,
                "error_code": error_code,
                "extra": self.extra
            }
        )



class ResourceNotFoundException(BaseAPIException):
    """Recurso não encontrado no banco de dados."""

    def __init__(self, resource: str, identifier: Any):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} com identificador '{identifier}' não encontrado.",
            error_code="RESOURCE_NOT_FOUND",
            extra={"resource": resource, "identifier": str(identifier)}
        )


class ProductNotFoundException(ResourceNotFoundException):
    """Produto não encontrado."""

    def __init__(self, product_id: int):
        super().__init__("Produto", product_id)


class CustomerNotFoundException(ResourceNotFoundException):
    """Cliente não encontrado."""

    def __init__(self, customer_id: int):
        super().__init__("Cliente", customer_id)


class ManufacturerNotFoundException(ResourceNotFoundException):
    """Fabricante não encontrado."""

    def __init__(self, manufacturer_id: int):
        super().__init__("Fabricante", manufacturer_id)


class SaleNotFoundException(ResourceNotFoundException):
    """Venda não encontrada."""

    def __init__(self, sale_id: int):
        super().__init__("Venda", sale_id)



class BusinessRuleException(BaseAPIException):
    """Violação de regra de negócio."""

    def __init__(self, detail: str, error_code: str = "BUSINESS_RULE_VIOLATION", extra: dict = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=detail,
            error_code=error_code,
            extra=extra
        )


class InsufficientStockException(BusinessRuleException):
    """Estoque insuficiente para realizar a operação."""

    def __init__(self, product_name: str, requested: int, available: int):
        super().__init__(
            detail=f"Estoque insuficiente para '{product_name}'. Solicitado: {requested}, Disponível: {available}.",
            error_code="INSUFFICIENT_STOCK",
            extra={
                "product": product_name,
                "requested_quantity": requested,
                "available_quantity": available
            }
        )


class NegativeStockException(BusinessRuleException):
    """Tentativa de definir estoque negativo."""

    def __init__(self, product_name: str, attempted_value: int):
        super().__init__(
            detail=f"O estoque de '{product_name}' não pode ser negativo (valor tentado: {attempted_value}).",
            error_code="NEGATIVE_STOCK_NOT_ALLOWED",
            extra={"product": product_name, "attempted_value": attempted_value}
        )


class InvalidPriceException(BusinessRuleException):
    """Preço inválido (negativo ou zero)."""

    def __init__(self, price: float):
        super().__init__(
            detail=f"Preço inválido: R$ {price:.2f}. O preço deve ser maior que zero.",
            error_code="INVALID_PRICE",
            extra={"price": price}
        )


class EmptySaleException(BusinessRuleException):
    """Venda sem itens."""

    def __init__(self):
        super().__init__(
            detail="A venda deve conter pelo menos 1 item.",
            error_code="EMPTY_SALE"
        )


class DuplicateResourceException(BusinessRuleException):
    """Recurso duplicado (e.g., email já cadastrado)."""

    def __init__(self, resource: str, field: str, value: str):
        super().__init__(
            detail=f"{resource} com {field} '{value}' já existe no sistema.",
            error_code="DUPLICATE_RESOURCE",
            extra={"resource": resource, "field": field, "value": value}
        )



class DatabaseException(BaseAPIException):
    """Erro genérico de banco de dados."""

    def __init__(self, detail: str = "Erro ao acessar o banco de dados."):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code="DATABASE_ERROR"
        )


class DatabaseConnectionException(DatabaseException):
    """Falha na conexão com o banco de dados."""

    def __init__(self):
        super().__init__(
            detail="Não foi possível conectar ao banco de dados. Tente novamente mais tarde."
        )



class AuthenticationException(BaseAPIException):
    """Erro de autenticação."""

    def __init__(self, detail: str = "Credenciais inválidas."):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code="AUTHENTICATION_FAILED"
        )


class AuthorizationException(BaseAPIException):
    """Erro de autorização (permissões)."""

    def __init__(self, detail: str = "Você não tem permissão para realizar esta ação."):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            error_code="AUTHORIZATION_FAILED"
        )



class InvalidInputException(BaseAPIException):
    """Entrada de dados inválida."""

    def __init__(self, field: str, reason: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Campo '{field}' inválido: {reason}",
            error_code="INVALID_INPUT",
            extra={"field": field, "reason": reason}
        )



class ExternalServiceException(BaseAPIException):

    def __init__(self, service_name: str, detail: str = None):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail or f"Falha ao comunicar com o serviço '{service_name}'.",
            error_code="EXTERNAL_SERVICE_ERROR",
            extra={"service": service_name}
        )