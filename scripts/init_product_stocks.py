import os
import sqlite3

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT_DIR, "orders.db")


conn = sqlite3.connect(DB_PATH)

try:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS product_stocks (
            product_stocks_id TEXT PRIMARY KEY,
            stock INTEGER
        )
    """)

    conn.commit()
finally:
    conn.close()

print("数据库和数据表初始化完成")
