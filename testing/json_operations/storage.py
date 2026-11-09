import json
import os
from pathlib import Path

ROOT = Path(os.environ.get("JSON_DATA", Path(__file__).parent))


def read(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def save(name, value):
    (ROOT / name).write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
