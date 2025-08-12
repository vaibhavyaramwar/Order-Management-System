import sqlite3

def insert_product(product):
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO Product (product_id, sku, product_name, price, stock_quantity, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (product.product_id, product.sku, product.product_name, product.price, product.stock_quantity, product.created_at))

    conn.commit()
    conn.close()

def get_products(limit=10, offset=0):
    """
    Fetch products with pagination.
    :param limit: Number of products to fetch.
    :param offset: Number of products to skip.
    :return: List of products.
    """
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Product LIMIT ? OFFSET ?', (limit, offset))
    products = cursor.fetchall()

    conn.close()
    return products

def get_total_product_count(limit=10, offset=0):
    """
    Get the total count of products in the database with limit and offset applied.
    :param limit: Number of products to fetch.
    :param offset: Number of products to skip.
    :return: Total product count with limit and offset applied.
    """
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM (SELECT * FROM Product LIMIT ? OFFSET ?)', (limit, offset))
    total_count = cursor.fetchone()[0]

    conn.close()
    return total_count

def delete_product_by_id(product_id: int):
    """
    Delete a product by its ID.
    :param product_id: ID of the product to delete.
    """
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM Product WHERE product_id = ?', (product_id,))
    conn.commit()

    conn.close()

def update_product_by_id(product_id: int, product):
    """
    Update a product by its ID.
    :param product_id: ID of the product to update.
    :param product: Product data to update.
    """
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE Product
        SET sku = ?, product_name = ?, price = ?, stock_quantity = ?, created_at = ?
        WHERE product_id = ?
    ''', (product.sku, product.product_name, product.price, product.stock_quantity, product.created_at, product_id))

    conn.commit()
    conn.close()

