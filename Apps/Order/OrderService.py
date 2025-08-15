from fastapi import FastAPI, HTTPException, status
from sqlalchemy.exc import IntegrityError
from Database import OrderDb, ProductDb, get_database_session
from Utils import CommonResponseUtil
from Modules.Order.model.OrderBO import StatusUpdate

app = FastAPI()

@app.post("/orders", status_code=status.HTTP_201_CREATED)
def create_order(order: OrderDb.Order):
    session = get_database_session()
    try:
        # Start a transaction
        product = session.query(ProductDb.Product).filter(ProductDb.Product.product_id == order.product_id).first()

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

        if product.stock_quantity < order.quantity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient stock")

        # Reduce stock
        product.stock_quantity -= order.quantity
        session.add(product)

        # Create order
        session.add(order)

        # Commit transaction
        session.commit()

        return CommonResponseUtil.create_common_response("SUCCESS", "Order created successfully", {"order": order})
    except HTTPException as e:
        session.rollback()
        raise e
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
    finally:
        session.close()

@app.get("/orders/{order_id}", status_code=status.HTTP_200_OK)
def get_order_by_id(order_id: int):
    """
    Fetch an order by its ID.
    :param order_id: ID of the order to fetch.
    :return: Order details or 404 if not found.
    """
    session = get_database_session()
    try:
        order = session.query(OrderDb.Order).filter(OrderDb.Order.order_id == order_id).first()

        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

        return CommonResponseUtil.create_common_response("SUCCESS", "Order fetched successfully", {"order": order})
    finally:
        session.close()

@app.put("/orders/{order_id}", status_code=status.HTTP_200_OK)
def update_order_status(order_id: int, status_update: StatusUpdate):
    """
    Update the status of an order.
    :param order_id: ID of the order to update.
    :param status_update: Pydantic model containing the new status.
    :return: Success message or validation error.
    """
    session = get_database_session()
    try:
        order = session.query(OrderDb.Order).filter(OrderDb.Order.order_id == order_id).first()

        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

        # Directly update the status using the validated Pydantic model
        order.status = status_update.status
        session.commit()

        return CommonResponseUtil.create_common_response("SUCCESS", "Order status updated successfully", {"order_id": order_id, "new_status": status_update.status})
    finally:
        session.close()

@app.delete("/orders/{order_id}", status_code=status.HTTP_200_OK)
def delete_order(order_id: int):
    """
    Delete an order if its status is not in terminal states.
    :param order_id: ID of the order to delete.
    :return: Success message or validation error.
    """
    session = get_database_session()
    try:
        order = session.query(OrderDb.Order).filter(OrderDb.Order.order_id == order_id).first()

        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

        # Check if the order is in a terminal state
        terminal_states = ['delivered', 'returned', 'refunded', 'cancelled', 'completed']
        if order.status in terminal_states:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete an order in a terminal state")

        # Delete the order
        session.delete(order)
        session.commit()

        return CommonResponseUtil.create_common_response("SUCCESS", "Order deleted successfully", {"order_id": order_id})
    finally:
        session.close()


