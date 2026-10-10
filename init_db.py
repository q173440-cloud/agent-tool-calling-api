import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "orders.db")

# 连接数据库，不存在时自动创建
conn = sqlite3.connect(DB_PATH)

try:
    # 创建示例数据表
    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            status TEXT
        )
    """)

    conn.commit()
finally:
    conn.close()

print("数据库和数据表初始化完成")
