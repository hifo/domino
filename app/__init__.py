"""Flask application factory for the Domino app."""
import requests

from flask import Flask, jsonify, render_template

from utils.utils import fetch_api_list, fetch_spell_detail


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
        except (requests.RequestException, ValueError):
            spells_level_1 = []
            spells_level_2 = []
            spells_level_3 = []
            spells_level_4 = []
            spells_level_5 = []
            spells_level_6 = []
        return render_template("index.html", spells_level_1=spells_level_1, spells_level_2=spells_level_2, spells_level_3=spells_level_3, spells_level_4=spells_level_4, spells_level_5=spells_level_5, spells_level_6=spells_level_6)

    @app.get("/spell/<path:spell_name>")
    def spell_detail(spell_name: str):
        try:
            return jsonify(fetch_spell_detail(spell_name))
        except (requests.RequestException, ValueError):
            return jsonify({"error": "Unable to load spell details"}), 502

    return app
