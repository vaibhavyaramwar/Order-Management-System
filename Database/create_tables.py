from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

def create_tables():
    engine = create_engine('sqlite:///ecommerce.db')
    Base.metadata.create_all(engine)

class Product(Base):
    __tablename__ = 'Product'

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    sku = Column(String, nullable=False, unique=True)
    product_name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)

    __table_args__ = (
        CheckConstraint('price > 0', name='check_price_positive'),
        CheckConstraint('stock_quantity >= 0', name='check_stock_non_negative'),
    )

class Order(Base):
    __tablename__ = 'Order'

    order_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('Product.product_id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)

    product = relationship('Product')

    __table_args__ = (
        CheckConstraint('quantity > 0', name='check_quantity_positive'),
    )