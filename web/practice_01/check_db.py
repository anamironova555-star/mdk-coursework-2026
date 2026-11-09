import sqlite3
from init_db import DB_PATH

conn = sqlite3.connect(DB_PATH)
try:
    print(
        "Таблицы:",
        conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall(),
    )
    print("Колонки:", conn.execute("PRAGMA table_info(tasks)").fetchall())
finally:
    conn.close()
