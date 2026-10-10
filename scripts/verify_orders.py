import os
import sqlite3

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT_DIR, "orders.db")

conn = sqlite3.connect(DB_PATH)
try:
    cursor = conn.execute("""
    SELECT *
    FROM orders
    """)
    jieguo = cursor.fetchall()
    print("当前订单数据:", jieguo)
finally:
    conn.close()
