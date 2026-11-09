import html
import importlib.util
import sqlite3
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def load(stage, name):
    path = ROOT / "web" / stage / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"{stage}_{name}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_init_is_idempotent(tmp_path):
    mod = load("practice_01", "init_db")
    db = tmp_path / "app.db"
    mod.init_db(db)
    mod.init_db(db)
    with sqlite3.connect(db) as conn:
        assert [r[1] for r in conn.execute("PRAGMA table_info(tasks)")] == [
            "id",
            "title",
            "status",
        ]
        conn.execute("INSERT INTO tasks(title) VALUES (?)", ("Тест",))
        assert conn.execute("SELECT status FROM tasks").fetchone()[0] == "new"
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute("INSERT INTO tasks(title) VALUES(NULL)")


def test_console_crud_and_injection(tmp_path):
    mod = load("practice_02", "crud_console")
    db = tmp_path / "app.db"
    mod.init_db(db)
    title = "'); DROP TABLE tasks; --"
    task_id = mod.add_task(title, db)
    assert mod.list_tasks(db)[0][1] == title
    assert mod.complete_task(task_id, db) == 1
    assert mod.list_tasks(db)[0][2] == "done"
    assert mod.delete_task(task_id, db) == 1
    assert mod.delete_task(task_id, db) == 0
    assert mod.list_tasks(db) == []
    with pytest.raises(ValueError):
        mod.add_task("  ", db)


def test_hello_routes():
    app = load("practice_03", "app").app
    client = app.test_client()
    assert client.get("/").status_code == 200
    assert b"Flask" in client.get("/").data
    assert client.get("/about").status_code == 200
    assert client.get("/nonexistent").status_code == 404
    assert client.post("/").status_code == 405


@pytest.mark.parametrize("stage", ["practice_04", "practice_05"])
def test_live_reading_and_escaping(stage, tmp_path):
    mod = load(stage, "app")
    app = mod.create_app(tmp_path / "app.db")
    client = app.test_client()
    assert "Список пуст" in client.get("/").text
    with sqlite3.connect(app.config["DATABASE"]) as conn:
        conn.execute(
            "INSERT INTO tasks(title,status) VALUES (?,?)",
            ("<script>alert(1)</script>", "done"),
        )
    page = client.get("/").text
    assert "&lt;script&gt;" in page and "<script>alert" not in page
    assert "done" in page
    assert client.get("/bad-route").status_code == 404


def test_post_validation_prg_and_persistence(tmp_path):
    mod = load("practice_05", "app")
    db = tmp_path / "app.db"
    app = mod.create_app(db)
    client = app.test_client()
    for title in ["", "   ", "x" * 201]:
        assert client.post("/", data={"title": title}).status_code == 400
    assert client.post("/", data={}).status_code == 400
    title = "'); DROP TABLE tasks; --"
    response = client.post("/", data={"title": title})
    assert response.status_code == 302 and response.location == "/"
    client.get("/")
    client.get("/")
    with sqlite3.connect(db) as conn:
        assert conn.execute("SELECT title FROM tasks").fetchall() == [(title,)]
    assert title in html.unescape(mod.create_app(db).test_client().get("/").text)


def test_database_failure_is_reported(tmp_path):
    mod = load("practice_05", "app")
    app = mod.create_app(tmp_path / "app.db")
    with sqlite3.connect(app.config["DATABASE"]) as conn:
        conn.execute("DROP TABLE tasks")
    response = app.test_client().post("/", data={"title": "Тест"})
    assert response.status_code == 503
    assert "баз" in response.text
