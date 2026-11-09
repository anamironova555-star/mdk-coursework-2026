import json
from storage import read

user = read("user.json")
print("Компактно:", json.dumps(user, ensure_ascii=False, separators=(",", ":")))
print("Отступы:", json.dumps(user, ensure_ascii=False, indent=2))
print("ASCII:", json.dumps(user, ensure_ascii=True))
print("Сортировка:", json.dumps(user, ensure_ascii=False, sort_keys=True))
