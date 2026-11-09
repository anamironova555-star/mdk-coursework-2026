from storage import read

u = read("user.json")
for k, t in {"id": int, "name": str, "email": str, "roles": list}.items():
    assert type(u[k]) is t
print("PASS: 04_types")
