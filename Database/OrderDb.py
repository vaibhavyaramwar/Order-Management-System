from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from transitions import Machine

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

class OrderStateMachine:
    states = ['PENDING', 'PROCESSING', 'COMPLETED', 'CANCELLED']

    def __init__(self, initial_state='PENDING'):
        self.state = initial_state

        # Initialize the state machine
        self.machine = Machine(model=self, states=OrderStateMachine.states, initial=initial_state)

        # Define transitions
        self.machine.add_transition(trigger='process', source='PENDING', dest='PROCESSING')
        self.machine.add_transition(trigger='complete', source='PROCESSING', dest='COMPLETED')
        self.machine.add_transition(trigger='cancel', source=['PENDING', 'PROCESSING'], dest='CANCELLED')

def update_order_status_with_state_machine(order_id: int, action: str):
    """
    Update the status of an order using a state machine.
    :param order_id: ID of the order to update.
    :param action: Action to perform (e.g., 'process', 'complete', 'cancel').
    """
    session = get_database_session()
    try:
        order = session.query(Order).filter(Order.order_id == order_id).first()

        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

        # Initialize the state machine with the current order status
        state_machine = OrderStateMachine(initial_state=order.status)

        # Perform the action
        if not hasattr(state_machine, action):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid action")

        getattr(state_machine, action)()

        # Update the order status
        order.status = state_machine.state
        session.commit()
    finally:
        session.close()