import argparse
from storage import read, save

parser = argparse.ArgumentParser()
parser.add_argument("--homework", action="store_true")
args = parser.parse_args()
user = read("user.json")
user["age"] = 26
user["city"] = "Санкт-Петербург"
user.setdefault("roles", [])
if "moderator" not in user["roles"]:
    user["roles"].append("moderator")
user.pop("active", None)
if args.homework:
    user["email"] = "ivan.new@mail.ru"
    user["phone"] = "+7-900-123-45-67"
    user.pop("roles", None)
save("user.json", user)
print(user)
