from storage import read, save

products = read("products.json")
report = {
    "total_value": round(sum(p["price"] * p["quantity"] for p in products), 2),
    "most_expensive": max(products, key=lambda p: p["price"])["name"]
    if products
    else None,
}
save("warehouse_report.json", report)
print(report)
