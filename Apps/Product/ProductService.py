from fastapi import FastAPI, HTTPException,status, Query

from Modules.Product.model import Product
from Database import ProductDb, create_tables
from Utils import CommonResponseUtil

app = FastAPI()

@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: Product.Product):
    # Here you would typically call a database function to save the product
    if create_tables.check_if_tables_exist()[0]:
        ProductDb.insert_product(product)
    else:
        create_tables.create_tables()
        ProductDb.insert_product(product)

    return CommonResponseUtil.create_common_response("SUCCESS", "Product created successfully", {"product": product})

@app.get("/products", status_code=status.HTTP_200_OK)
def get_products(limit: int = Query(10, ge=1), offset: int = Query(0, ge=0)):

    products = ProductDb.get_products(limit=limit, offset=offset)
    total_count = ProductDb.get_total_product_count()

    response_data = {
        "products": products,
        "pagination": {
            "total_count": total_count,
            "limit": limit,
            "offset": offset
        }
    }

    return CommonResponseUtil.create_common_response("SUCCESS", "Products fetched successfully", response_data)

@app.get("/products/{product_id}", status_code=status.HTTP_200_OK)
def get_product_by_id(product_id: int):
    """
    Fetch a product by its ID.
    :param product_id: ID of the product to fetch.
    :return: Product details or 404 if not found.
    """
    product = ProductDb.get_product_by_id(product_id)

    if not product:
        response = CommonResponseUtil.create_common_response("ERROR", "Product Not Found", {"product": product})
        raise HTTPException(status_code=404, detail=response)


    return CommonResponseUtil.create_common_response("SUCCESS", "Product fetched successfully", {"product": product})


@app.delete("/products/{product_id}", status_code=status.HTTP_200_OK)
def delete_product(product_id: int):
    """
    Delete a product by its ID.
    :param product_id: ID of the product to delete.
    :return: Success message or 404 if not found.
    """
    product = ProductDb.get_product_by_id(product_id)

    if not product:
        return CommonResponseUtil.create_common_response("FAILURE", "Product not found", {}, status_code=status.HTTP_404_NOT_FOUND)

    ProductDb.delete_product_by_id(product_id)
    return CommonResponseUtil.create_common_response("SUCCESS", "Product deleted successfully", {})


@app.put("/products/{product_id}", status_code=status.HTTP_200_OK)
def update_product(product_id: int, product: Product.Product):
    """
    Update a product by its ID.
    :param product_id: ID of the product to update.
    :param product: Product data to update.
    :return: Success message or 404 if not found.
    """
    existing_product = ProductDb.get_product_by_id(product_id)

    if not existing_product:
        return CommonResponseUtil.create_common_response("FAILURE", "Product not found", {}, status_code=status.HTTP_404_NOT_FOUND)

    ProductDb.update_product_by_id(product_id, product)
    return CommonResponseUtil.create_common_response("SUCCESS", "Product updated successfully", {"product": product})
