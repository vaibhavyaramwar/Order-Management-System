from pydantic import BaseModel, Field, validator

'''
price should be greater than 0
stock_quantity should be greater than or equal to 0
product_name should not be empty
sku should not be empty
product_id should be a positive integer
product_id should be unique
created_at should be a valid date format
'''

class Product(BaseModel):
    product_id: int = Field(..., description="Unique identifier for the product")
    sku: str = Field(..., description="Stock Keeping Unit for the product")
    product_name: str = Field(..., ,description="Name of the product")
    price: float = Field(..., gt=0,description="Price of the product")
    stock_quantity: int = Field(..., gteq=0,description="Quantity of the product available in stock")
    created_at: str = Field(..., description="Date when the product was added")

@validator('product_name')
def product_name_must_not_be_empty(cls, value: str) -> str:
    if not value.strip():
        raise ValueError("Product name must not be empty")
    return value

@validator('sku')
def sku_must_not_be_empty(cls, value: str) -> str:
    if not value.strip():
        raise ValueError("SKU must not be empty")
    return value

@validator('product_id')
def product_id_must_be_positive(cls, value: int) -> int:
    if value <= 0:
        raise ValueError("Product ID must be a positive integer")
    return value