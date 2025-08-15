from sqlalchemy import create_engine, Column, Integer, String, Float,DateTime, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

def get_database_session():
    engine = create_engine('sqlite:///ecommerce.db')
    Session = sessionmaker(bind=engine)
    return Session()

class Product(Base):
    __tablename__ = 'Product'

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    sku = Column(String, nullable=False)
    product_name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)

Base.metadata.create_all(create_engine('sqlite:///ecommerce.db'))

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
Base.metadata.create_all(create_engine('sqlite:///ecommerce.db'))

def insert_product(product):
    session = get_database_session()
    session.add(product)
    session.commit()
    session.close()

def get_products(limit=10, offset=0):
    session = get_database_session()
    products = session.query(Product).limit(limit).offset(offset).all()
    session.close()
    return products

def get_total_product_count():
    session = get_database_session()
    total_count = session.query(Product).count()
    session.close()
    return total_count

def delete_product_by_id(product_id: int):
    session = get_database_session()
    product = session.query(Product).filter(Product.product_id == product_id).first()
    if product:
        session.delete(product)
        session.commit()
    session.close()

def update_product_by_id(product_id: int, product_data):
    session = get_database_session()
    product = session.query(Product).filter(Product.product_id == product_id).first()
    if product:
        product.sku = product_data.sku
        product.product_name = product_data.product_name
        product.price = product_data.price
        product.stock_quantity = product_data.stock_quantity
        product.created_at = product_data.created_at
        session.commit()
    session.close()
    

def insert_order(order):
    session = get_database_session()
    session.add(order)
    session.commit()
    session.close()