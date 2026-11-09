import argparse
import json
import math
import re
from pathlib import Path


def pairs_unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Дубликат ключа: {key}")
        result[key] = value
    return result


def load(path):
    def reject(value):
        raise ValueError(f"Недопустимая константа: {value}")

    return json.loads(
        Path(path).read_text(encoding="utf-8"),
        object_pairs_hook=pairs_unique,
        parse_constant=reject,
    )


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_users(value):
    require(type(value) is dict and set(value) == {"users"}, "Корень users")
    users = value["users"]
    require(type(users) is list and len(users) == 3, "Нужны 3 пользователя")
    ids = set()
    for user in users:
        require(
            type(user) is dict and set(user) == {"id", "name", "email", "active"},
            "Поля пользователя",
        )
        require(type(user["id"]) is int and user["id"] > 0, "ID — положительное целое")
        require(user["id"] not in ids, "ID повторяется")
        ids.add(user["id"])
        require(type(user["name"]) is str and bool(user["name"].strip()), "Пустое имя")
        require(
            type(user["email"]) is str
            and re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", user["email"]) is not None,
            "Формат email",
        )
        require(type(user["active"]) is bool, "active — bool")


def validate_config(value):
    require(
        type(value) is dict and set(value) == {"server", "database", "logging"},
        "Секции конфига",
    )
    for section, fields in {
        "server": {"host", "port", "timeout"},
        "database": {"host", "port", "name"},
        "logging": {"level", "file"},
    }.items():
        require(
            type(value[section]) is dict and set(value[section]) == fields,
            f"Поля {section}",
        )
    for section in ["server", "database"]:
        port = value[section]["port"]
        require(type(port) is int and 1 <= port <= 65535, "Порт вне диапазона")
        require(
            type(value[section]["host"]) is str and bool(value[section]["host"]),
            "host — строка",
        )
    timeout = value["server"]["timeout"]
    require(
        type(timeout) is int and timeout > 0, "timeout должен быть положительным целым"
    )
    require(
        type(value["database"]["name"]) is str
        and bool(value["database"]["name"].strip()),
        "Пустая БД",
    )
    require(
        value["logging"]["level"] in ["DEBUG", "INFO", "WARNING", "ERROR"],
        "Уровень логирования",
    )
    require(
        type(value["logging"]["file"]) is str
        and value["logging"]["file"].startswith("/"),
        "Путь лога",
    )


def validate_orders(value):
    require(type(value) is dict and set(value) == {"orders"}, "Корень orders")
    orders = value["orders"]
    require(type(orders) is list and len(orders) == 3, "Нужны 3 заказа")
    ids = set()
    for order in orders:
        require(
            type(order) is dict and set(order) == {"id", "user_id", "amount", "status"},
            "Поля заказа",
        )
        for key in ["id", "user_id"]:
            require(
                type(order[key]) is int and order[key] > 0, "ID заказа/пользователя"
            )
        require(order["id"] not in ids, "ID заказа повторяется")
        ids.add(order["id"])
        require(
            type(order["amount"]) in (int, float)
            and math.isfinite(order["amount"])
            and order["amount"] > 0,
            "Сумма заказа",
        )
        require(order["status"] in ["paid", "pending", "cancelled"], "Статус заказа")


def validate_products(value):
    require(type(value) is dict and set(value) == {"products"}, "Корень products")
    products = value["products"]
    require(type(products) is list and len(products) == 5, "Нужны 5 товаров")
    ids = set()
    for product in products:
        require(
            type(product) is dict
            and set(product) == {"id", "name", "price", "in_stock"},
            "Поля товара",
        )
        require(
            type(product["id"]) is int
            and product["id"] > 0
            and product["id"] not in ids,
            "ID товара",
        )
        ids.add(product["id"])
        require(
            type(product["name"]) is str and bool(product["name"].strip()), "Имя товара"
        )
        require(
            type(product["price"]) in (int, float)
            and math.isfinite(product["price"])
            and product["price"] > 0,
            "Цена товара",
        )
        require(type(product["in_stock"]) is bool, "in_stock — bool")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "kind", choices=["users", "config", "orders", "products", "syntax"]
    )
    parser.add_argument("file", type=Path)
    args = parser.parse_args()
    try:
        value = load(args.file)
        if args.kind != "syntax":
            globals()[f"validate_{args.kind}"](value)
        print(f"PASS: {args.kind} {args.file.name}")
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(f"FAIL: {exc}")
        raise SystemExit(1)
