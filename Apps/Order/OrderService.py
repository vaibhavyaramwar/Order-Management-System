from fastapi import FastAPI, HTTPException, status
from sqlalchemy.exc import IntegrityError
from Database import OrderDb, ProductDb
from Database.OrderDb import get_database_session
from Utils import CommonResponseUtil
from Modules.Order.model import OrderBO
from Modules.Product.model import ProductBO
from Apps.Response.OrderResponse import OrderResponse
from Apps.Response.ProductResponse import ProductResponse
from Utils.OrderStatus import OrderStatus
from Database.OrderDb import Order

app = FastAPI()

@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductBO.ProductBO):
    session = get_database_session()
    try:
        if not session.query(OrderDb.Product).filter(OrderDb.Product.sku == product.sku).first():
            new_product = OrderDb.Product(
                sku=product.sku,
                product_name=product.product_name,
                price=product.price,
                stock_quantity=product.stock_quantity,
                created_at=product.created_at
            )
            session.add(new_product)
            session.commit()
            productResponse = ProductResponse(
                product_id=new_product.product_id,
                sku=new_product.sku,
                product_name=new_product.product_name,
                price=new_product.price,
                stock_quantity=new_product.stock_quantity,
                created_at=new_product.created_at
            )
            return CommonResponseUtil.create_common_response("SUCCESS", "Product created successfully", {"product": productResponse})
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product with this SKU already exists")
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
    finally:
        session.close()

@app.get("/products", status_code=status.HTTP_200_OK)
def get_products(limit: int = 10, offset: int = 0):
    session = get_database_session()
    try:
        products = session.query(OrderDb.Product).limit(limit).offset(offset).all()
        total_count = session.query(OrderDb.Product).count()

        response_data = {
            "products": products,
            "pagination": {
                "total_count": total_count,
                "limit": limit,
                "offset": offset
            }
        }

        return CommonResponseUtil.create_common_response("SUCCESS", "Products fetched successfully", response_data)
    finally:
        session.close()

@app.get("/products/{product_id}", status_code=status.HTTP_200_OK)
def get_product_by_id(product_id: int):
    session = get_database_session()
    try:
        product = session.query(OrderDb.Product).filter(OrderDb.Product.product_id == product_id).first()

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

        return CommonResponseUtil.create_common_response("SUCCESS", "Product fetched successfully", {"product": product})
    finally:
        session.close()

# delete product by id
@app.delete("/products/{product_id}", status_code=status.HTTP_200_OK)
def delete_product(product_id: int):
    session = get_database_session()
    try:
        product = session.query(OrderDb.Product).filter(OrderDb.Product.product_id == product_id).first()

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

        session.delete(product)
        session.commit()
        return CommonResponseUtil.create_common_response("SUCCESS", "Product deleted successfully", {"product_id": product_id})
    finally:
        session.close()

@app.post("/orders", response_model=None,status_code=status.HTTP_201_CREATED)
def create_order(order: OrderBO.OrderBo):
    session = get_database_session()
    try:
        # Start a transaction
        product = session.query(OrderDb.Product).filter(OrderDb.Product.product_id == order.product_id).first()

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

        if product.stock_quantity < order.quantity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient stock")

        # Reduce stock
        product.stock_quantity -= order.quantity
        session.add(product)

        OrderDb.Order = OrderDb.Order(
            product_id=order.product_id,
            quantity=order.quantity,
            status=order.status,
            created_at=order.created_at
        )

        # Create order
        session.add(OrderDb.Order)

        # Commit transaction
        session.commit()

        orderResponse = OrderResponse(
            order_id=OrderDb.Order.order_id,
            product_id=order.product_id,
            quantity=order.quantity,
            status=order.status,
            created_at=order.created_at
        )

        #return OrderResponse
        return CommonResponseUtil.create_common_response("SUCCESS", "Order created successfully", {"order": orderResponse})
    except HTTPException as e:
        session.rollback()
        raise e
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
    finally:
        session.close()

# get order by id
@app.get("/orders/{order_id}", response_model=None, status_code=status.HTTP_200_OK)
def get_order_by_id(order_id: int):
    """
    Fetch an order by its ID.
    :param order_id: ID of the order to fetch.
    :return: Order details or 404 if not found.
    """
    session = get_database_session()
    try:
        #order = session.query(OrderDb.Order).filter(OrderDb.Order.order_id == order_id).first()
        order = session.query(Order).filter(Order.order_id == order_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

        orderResponse = OrderResponse(
            order_id=order.order_id,
            product_id=order.product_id,
            quantity=order.quantity,
            status=order.status,
            created_at=order.created_at
        )

        return CommonResponseUtil.create_common_response("SUCCESS", "Order fetched successfully", {"order": orderResponse})
    finally:
        session.close()

@app.put("/orders/{order_id}", response_model=None,status_code=status.HTTP_200_OK)
def update_order_status(order_id: int, status_update: str):
    """
    Update the status of an order.
    :param order_id: ID of the order to update.
    :param status_update: Pydantic model containing the new status.
    :return: Success message or validation error.
    """
    session = get_database_session()
    try:
        #order = session.query(OrderDb.Order).filter(OrderDb.Order.order_id == order_id).first()
        order = session.query(Order).filter(Order.order_id == order_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

        # Validate the new status using the OrderStatus Enum
        if status_update not in [status.value for status in OrderStatus]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid status. Must be one of {[status.value for status in OrderStatus]}")

        # Directly update the status using the validated Pydantic model
        order.status = status_update
        session.commit()

        return CommonResponseUtil.create_common_response("SUCCESS", "Order status updated successfully", {"order_id": order_id, "new_status": status_update})
    finally:
        session.close()

@app.delete("/orders/{order_id}", response_model=None,status_code=status.HTTP_200_OK)
def delete_order(order_id: int):
    """
    Delete an order if its status is not in terminal states.
    :param order_id: ID of the order to delete.
    :return: Success message or validation error.
    """
    session = get_database_session()
    try:
        #order = session.query(OrderDb.Order).filter(OrderDb.Order.order_id == order_id).first()
        order = session.query(Order).filter(Order.order_id == order_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

        # Check if the order status is in terminal states
        if order.status in [OrderStatus.DELIVERED.value, OrderStatus.CANCELLED.value]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete order in terminal state")
 
        session.delete(order)
        session.commit()
        return CommonResponseUtil.create_common_response("SUCCESS", "Order deleted successfully", {"order_id": order_id})
    finally:
        session.close()