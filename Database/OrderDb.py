from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

def get_database_session():
    engine = create_engine('sqlite:///ecommerce.db')
    Session = sessionmaker(bind=engine)
    return Session()

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

def insert_order(order):
    session = get_database_session()
    session.add(order)
    session.commit()
    session.close()