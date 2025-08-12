import sqlite3

'''
create table order and product
refer Modules/Product/model/Product.py and Modules/Order/model/Order.py
'''

def create_tables():
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()

    # Create Product table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Product (
            product_id INTEGER PRIMARY KEY,
            sku TEXT NOT NULL UNIQUE,
            product_name TEXT NOT NULL,
            price REAL NOT NULL CHECK(price > 0),
            stock_quantity INTEGER NOT NULL CHECK(stock_quantity >= 0),
            created_at TEXT NOT NULL
        )
    ''')

    # Create Order table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Order (
            order_id INTEGER PRIMARY KEY,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL CHECK(quantity > 0),
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (product_id) REFERENCES Product(product_id)
        )
    ''')

    conn.commit()
    conn.close()

def check_if_tables_exist():
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()      

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Product'")
    product_exists = cursor.fetchone() is not None

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Order'")
    order_exists = cursor.fetchone() is not None

    conn.close()
    
    return product_exists, order_exists

def insert_product(product):
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO Product (product_id, sku, product_name, price, stock_quantity, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (product.product_id, product.sku, product.product_name, product.price, product.stock_quantity, product.created_at))

    conn.commit()
    conn.close()

def insert_order(order):
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO Order (order_id, product_id, quantity, status, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (order.order_id, order.product_id, order.quantity, order.status, order.created_at))

    conn.commit()
    conn.close()