from storage import read

u = read("user.json")
assert u["id"] == 1 and u["email"].endswith("@mail.ru") and "admin" in u["roles"]
print("PASS: 05_values")
