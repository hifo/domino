"""Flask application factory for the Domino app."""
from flask import Flask, render_template

from utils.utils import fetch_api_list


def create_app() -> Flask:
    app = Flask(__name__)
    app.jinja_env.globals["fetch_api_list"] = fetch_api_list

    @app.get("/")
    def index() -> str:
        try:
            spells_level_1 = fetch_api_list(spell_level=1)
            spells_level_2 = fetch_api_list(spell_level=2)
            spells_level_3 = fetch_api_list(spell_level=3)
            spells_level_4 = fetch_api_list(spell_level=4)
            spells_level_5 = fetch_api_list(spell_level=5)
            spells_level_6 = fetch_api_list(spell_level=6)
        except Exception:
            spells_level_1 = []
            spells_level_2 = []
            spells_level_3 = []
            spells_level_4 = []
            spells_level_5 = []
            spells_level_6 = []
        return render_template("index.html", spells_level_1=spells_level_1, spells_level_2=spells_level_2, spells_level_3=spells_level_3, spells_level_4=spells_level_4, spells_level_5=spells_level_5, spells_level_6=spells_level_6)

    return app
