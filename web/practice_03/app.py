import os
from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return '<h1>Hello, Flask!</h1><p>Первый маршрут работает.</p><a href="/about">О проекте</a>'


@app.route("/about")
def about():
    return '<h1>О проекте</h1><p>Учебное приложение на Flask. Практика №3.</p><a href="/">Главная</a>'


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=int(os.environ.get("PORT", "5000")),
        debug=os.environ.get("FLASK_DEBUG") == "1",
    )
