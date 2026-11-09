import argparse
import sqlite3
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--workspace", type=Path, default=Path("ddl_demo"))
args = parser.parse_args()
args.workspace.mkdir(parents=True, exist_ok=True)
for mode in ["implicit", "explicit"]:
    path = args.workspace / f"{mode}.db"
    conn = sqlite3.connect(path)
    if mode == "explicit":
        conn.execute("BEGIN")
    conn.execute("CREATE TABLE demo(id INTEGER)")
    conn.close()
    conn = sqlite3.connect(path)
    present = bool(
        conn.execute("SELECT name FROM sqlite_master WHERE name='demo'").fetchone()
    )
    conn.close()
    print(f"{mode}: table persists without commit = {present}")
    if present != (mode == "implicit"):
        raise SystemExit(1)
print("PASS: DDL transaction behavior verified")
