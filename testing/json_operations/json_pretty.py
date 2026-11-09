import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("filename", type=Path)
args = parser.parse_args()
try:
    value = json.loads(args.filename.read_text(encoding="utf-8"))
    args.filename.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("Отформатирован:", args.filename)
except (OSError, ValueError) as exc:
    parser.exit(1, f"Ошибка: {exc}\n")
