from storage import save

user = {
    "id": 1,
    "name": "Иван",
    "email": "ivan@mail.ru",
    "age": 25,
    "active": True,
    "roles": ["admin", "user"],
}
save("user.json", user)
print("Создан user.json:", user)
