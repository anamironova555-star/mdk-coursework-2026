import os
import sqlite3
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for


def create_app(db_path=None):
    app = Flask(__name__, root_path=str(Path(__file__).parent))
    app.config["DATABASE"] = str(
        db_path or os.environ.get("TASK_DB", Path(__file__).with_name("app.db"))
    )
    conn = sqlite3.connect(app.config["DATABASE"])
    try:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL, status TEXT DEFAULT 'new')"
        )
        conn.commit()
    finally:
        conn.close()

    def fetch_all_tasks():
        conn = sqlite3.connect(app.config["DATABASE"])
        conn.row_factory = sqlite3.Row
        try:
            return conn.execute(
                "SELECT id,title,status FROM tasks ORDER BY id"
            ).fetchall()
        finally:
            conn.close()

    @app.route("/", methods=["GET", "POST"])
    def index():
        try:
            if request.method == "POST":
                title = request.form.get("title", "").strip()
                if not title or len(title) > 200:
                    return render_template(
                        "index.html",
                        items=fetch_all_tasks(),
                        error="Введите название от 1 до 200 символов.",
                    ), 400
                conn = sqlite3.connect(app.config["DATABASE"])
                try:
                    conn.execute("INSERT INTO tasks(title) VALUES (?)", (title,))
                    conn.commit()
                except sqlite3.Error:
                    conn.rollback()
                    raise
                finally:
                    conn.close()
                return redirect(url_for("index"))
            return render_template("index.html", items=fetch_all_tasks())
        except sqlite3.Error:
            app.logger.exception("Ошибка SQLite")
            return render_template(
                "index.html",
                items=[],
                error="Не удалось обратиться к базе данных. Повторите запрос позже.",
            ), 503

    return app


if __name__ == "__main__":
    create_app().run(
        host="127.0.0.1",
        port=int(os.environ.get("PORT", "5000")),
        debug=os.environ.get("FLASK_DEBUG") == "1",
    )
