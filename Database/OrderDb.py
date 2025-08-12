import sqlite3

def insert_order(order):
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO Order (order_id, product_id, quantity, status, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (order.order_id, order.product_id, order.quantity, order.status, order.created_at))

    conn.commit()
    conn.close()