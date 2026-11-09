import importlib.util
from pathlib import Path

import pytest

PATH = Path(__file__).resolve().parents[1] / "testing/json_validation/validate.py"
spec = importlib.util.spec_from_file_location("validator", PATH)
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
DATA = PATH.parent / "data"


@pytest.mark.parametrize("kind", ["users", "config", "orders", "products"])
def test_valid_fixtures(kind):
    getattr(v, f"validate_{kind}")(v.load(DATA / f"{kind}.json"))


@pytest.mark.parametrize(
    "case",
    [
        "duplicate_id",
        "extra_field",
        "missing_field",
        "wrong_type",
        "bad_email",
        "bool_id",
    ],
)
def test_invalid_users(case):
    users = v.load(DATA / "users.json")
    u = users["users"][0]
    if case == "duplicate_id":
        users["users"][1]["id"] = u["id"]
    elif case == "extra_field":
        u["password"] = "secret"
    elif case == "missing_field":
        del u["name"]
    elif case == "wrong_type":
        u["active"] = "true"
    elif case == "bad_email":
        u["email"] = "a@"
    else:
        u["id"] = True
    with pytest.raises(ValueError):
        v.validate_users(users)


@pytest.mark.parametrize("port", [0, 65536, "8080", True, 3.14])
def test_invalid_ports(port):
    config = v.load(DATA / "config.json")
    config["server"]["port"] = port
    with pytest.raises(ValueError):
        v.validate_config(config)


@pytest.mark.parametrize(
    "text", ['{"a":1,"a":2}', '{"a":1,}', '{"a":NaN}', '{"a":Infinity}']
)
def test_invalid_json(text, tmp_path):
    path = tmp_path / "bad.json"
    path.write_text(text)
    with pytest.raises(ValueError):
        v.load(path)


def test_invalid_encoding(tmp_path):
    path = tmp_path / "bad.json"
    path.write_bytes(b'{"a":"\xff"}')
    with pytest.raises(UnicodeDecodeError):
        v.load(path)


@pytest.mark.parametrize(
    "kind,field,bad",
    [
        ("orders", "amount", -1),
        ("orders", "status", "unknown"),
        ("products", "price", True),
        ("products", "in_stock", 1),
    ],
)
def test_invalid_business_values(kind, field, bad):
    value = v.load(DATA / f"{kind}.json")
    value[kind][0][field] = bad
    with pytest.raises(ValueError):
        getattr(v, f"validate_{kind}")(value)
