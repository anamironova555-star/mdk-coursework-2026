from storage import read, save

users = read("users.json")
report = {
    "total": len(users),
    "active": sum(user["active"] for user in users),
    "average_age": sum(user["age"] for user in users) / len(users) if users else 0,
    "adults": [user["name"] for user in users if user["age"] >= 18],
    "oldest": max(users, key=lambda user: user["age"])["name"] if users else None,
    "under_18": sum(user["age"] < 18 for user in users),
}
save("users_report.json", report)
print(report)
