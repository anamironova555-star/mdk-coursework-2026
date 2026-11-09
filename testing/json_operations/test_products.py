from storage import read

p = read("products.json")
assert len({x["id"] for x in p}) == len(p)
for x in p:
    assert {"id", "name", "price", "quantity"} <= x.keys()
    assert type(x["price"]) in (int, float) and x["price"] > 0
    assert type(x["quantity"]) is int and x["quantity"] >= 0
print("PASS: products")
