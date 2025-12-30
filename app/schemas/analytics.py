from pydantic import BaseModel

class TopCustomerResponse(BaseModel):
    customer_id: int
    customer_name: str
    total_spent: float
    order_count: int

    class Config:
        from_attributes = True

class ProductSalesResponse(BaseModel):
    product_id: int
    product_name: str
    total_quantity_sold: int
    total_revenue: float

    class Config:
        from_attributes = True

class ManufacturerRankingResponse(BaseModel):
    manufacturer_id: int
    manufacturer_name: str
    total_sales_value: float
    products_sold_count: int

    class Config:
        from_attributes = True

class GlobalKPIsResponse(BaseModel):
    total_revenue: float
    total_orders: int
    average_ticket: float

class SalesByCategoryResponse(BaseModel):
    category: str
    total_sold: int

    class Config:
        from_attributes = True

class GlobalKPIsResponse(BaseModel):
    total_revenue: float
    revenue_delta: float  # Novo campo para a variação
    total_orders: int
    orders_delta: int     # Novo campo
    average_ticket: float
    ticket_delta: float   # Novo campo