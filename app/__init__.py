from flask import Flask, render_template


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def index() -> str:
        return render_template("index.html")

    return app
