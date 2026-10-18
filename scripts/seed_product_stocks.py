import os
import sqlite3

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT_DIR, "orders.db")

conn = sqlite3.connect(DB_PATH)
try:
    product_stocks = [
        ["P001", 12],
        ["P002", 0],
        ["P003", 5]
    ]
    conn.executemany("""
        INSERT OR REPLACE INTO product_stocks (product_stocks_id, stock)
        VALUES (?, ?)
    """, product_stocks)
    conn.commit()
    cursor = conn.execute("""
    SELECT *
    FROM product_stocks
    """)
    jieguo = cursor.fetchall()
    print("种子数据初始化完成:", jieguo)
finally:
    conn.close()
