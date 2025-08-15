from pydantic import BaseModel, Field, validator
from datetime import date

class OrderBo(BaseModel):
    product_id: int = Field(..., gt=0, description="Unique identifier for the product")
    quantity: int = Field(..., gt=0, description="Quantity of the product ordered")
    status: str = Field(..., description="Current status of the order (e.g., PENDING, SHIPPED, DELIVERED, CANCELLED, PAID)")
    created_at: date = Field(..., description="Date when the order was placed")