from storage import read

assert {"id", "name", "email", "roles"} <= read("user.json").keys()
print("PASS: 03_fields")
