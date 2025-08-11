from pydantic import BaseModel, Field, validator

class Order(BaseModel):
    order_id: int = Field(..., description="Unique identifier for the order")
    product_id: int = Field(..., description="Unique identifier for the product")
    quantity: int = Field(..., description="Quantity of the product ordered")
    status: str = Field(..., description="Current status of the order (e.g., PENDING, SHIPPED, DELIVERED,CANCELLED,PAID)")
    created_at: str = Field(..., description="Date when the order was placed")
    

@validator('status')
def status_must_be_valid(cls, value: str) -> str:
    valid_statuses = {"PENDING", "SHIPPED", "DELIVERED", "CANCELLED", "PAID"}
    if value not in valid_statuses:
        raise ValueError(f"Status must be one of {valid_statuses}")
    return value

@validator('order_id')
def order_id_must_be_positive(cls, value: int) -> int:
    if value <= 0:
        raise ValueError("Order ID must be a positive integer")
    return value

@validator('product_id')
def product_id_must_be_positive(cls, value: int) -> int:
    if value <= 0:
        raise ValueError("Product ID must be a positive integer")
    return value

@validator('created_at')
def created_at_must_be_valid_date(cls, value: str) -> str:
    from datetime import datetime
    try:
        datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise ValueError("Created at must be in the format YYYY-MM-DD HH:MM:SS")
    return value

@validator('quantity')
def quantity_must_be_positive(cls, value: int) -> int:
    if value <= 0:
        raise ValueError("Quantity must be a positive integer")
    return value

@validator('created_at')
def created_at_must_not_be_empty(cls, value: str) -> str:
    if not value.strip():
        raise ValueError("Created at must not be empty")
    return value

@validator('product_id')
def product_id_must_not_be_empty(cls, value: int) -> int:
    if value is None:
        raise ValueError("Product ID must not be empty")
    return value

@validator('order_id')
def order_id_must_not_be_empty(cls, value: int) -> int:
    if value is None:
        raise ValueError("Order ID must not be empty")
    return value

@validator('status')
def status_must_not_be_empty(cls, value: str) -> str:
    if not value.strip():
        raise ValueError("Status must not be empty")
    return value

@validator('created_at')
def created_at_must_not_be_empty(cls, value: str) -> str:
    if not value.strip():
        raise ValueError("Created at must not be empty")
    return value

@validator('quantity')
def quantity_must_not_be_empty(cls, value: int) -> int:
    if value is None:
        raise ValueError("Quantity must not be empty")
    return value

@validator('product_id')
def product_id_must_be_unique(cls, value: int, values: dict) -> int:
    if 'product_id' in values and value in values['product_id']:
        raise ValueError("Product ID must be unique")
    return value

@validator('order_id')
def order_id_must_be_unique(cls, value: int, values: dict) -> int:
    if 'order_id' in values and value in values['order_id']:
        raise ValueError("Order ID must be unique")
    return value

@validator('product_id')
def product_id_must_exist(cls, value: int, values: dict) -> int:
    if 'product_id' in values and value not in values['product_id']:
        raise ValueError("Product ID must exist in the product database")
    return value

@validator('order_id')
def order_id_must_exist(cls, value: int, values: dict) -> int:
    if 'order_id' in values and value not in values['order_id']:
        raise ValueError("Order ID must exist in the order database")
    return value

@validator('quantity')
def quantity_must_be_available(cls, value: int, values: dict) -> int:
    if 'product_id' in values and value > values['product_id'].stock_quantity:
        raise ValueError("Quantity ordered exceeds available stock")
    return value

@validator('status')
def status_must_be_valid(cls, value: str) -> str:
    valid_statuses = {"PENDING", "SHIPPED", "DELIVERED", "CANCELLED", "PAID"}
    if value not in valid_statuses:
        raise ValueError(f"Status must be one of {valid_statuses}")
    return value

@validator('created_at')
def created_at_must_be_valid(cls, value: str) -> str:
    from datetime import datetime
    try:
        datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise ValueError("Created at must be in the format YYYY-MM-DD HH:MM:SS")
    return value

@validator('quantity')
def quantity_must_be_positive(cls, value: int) -> int:
    if value <= 0:
        raise ValueError("Quantity must be a positive integer")
    return value

@validator('created_at')
def created_at_must_not_be_empty(cls, value: str) -> str:
    if not value.strip():
        raise ValueError("Created at must not be empty")
    return value