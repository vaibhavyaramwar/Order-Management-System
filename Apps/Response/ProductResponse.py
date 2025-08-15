from pydantic import BaseModel, Field, validator
from datetime import datetime

class ProductResponse(BaseModel):
    product_id : int
    sku : str
    product_name : str
    price : float
    stock_quantity : int
    created_at : datetime