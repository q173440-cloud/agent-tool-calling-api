import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "orders.db")

conn = sqlite3.connect(DB_PATH)
try:
    orders = [
        ["A1001", "已发货"],
        ["A1002", "处理中"],
        ["A1003", "已完成"]
    ]
    conn.executemany("""
        INSERT OR REPLACE INTO orders (order_id, status)
        VALUES (?, ?)
    """, orders)
    conn.commit()
    cursor = conn.execute("""
    SELECT *
    FROM orders
    """)
    jieguo = cursor.fetchall()
    print("种子数据初始化完成:", jieguo)
finally:
    conn.close()
