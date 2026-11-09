from storage import read

user = read("user.json")
print("Имя:", user["name"])
print("Возраст:", user["age"])
print("Email:", user["email"])
print("Роли:", user.get("roles", []))
print("Всего ролей:", len(user.get("roles", [])))
print("Активен:", user.get("active", False))
print("Ключей:", len(user))
print("Телефон:", user.get("phone", "не указан"))
