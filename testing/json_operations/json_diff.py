import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("first", type=Path)
parser.add_argument("second", type=Path)
args = parser.parse_args()
try:
    first, second = [
        json.loads(p.read_text(encoding="utf-8")) for p in [args.first, args.second]
    ]
    if not isinstance(first, dict) or not isinstance(second, dict):
        raise ValueError("Оба корня должны быть объектами")
    print("Только в первом:", sorted(first.keys() - second.keys()))
    print("Только во втором:", sorted(second.keys() - first.keys()))
except (OSError, ValueError) as exc:
    parser.exit(1, f"Ошибка: {exc}\n")
