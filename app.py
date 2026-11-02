import json
from flask import Flask, jsonify, abort, render_template
from pathlib import Path
import random

app = Flask(__name__)

# Load the content file once, when the app starts
BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR / "content.json", encoding="utf-8") as file:
    content = json.load(file)
    

@app.route("/")
def home():
    return render_template("index.html", categories=list(content.keys()))


@app.route("/categories")
def get_categories():
    return jsonify(list(content.keys()))

@app.route("/categories/<category_name>")
def get_situations(category_name):
    if category_name not in content:
        abort(404)
    return jsonify(list(content[category_name].keys()))

@app.route("/categories/<category_name>/<situation_name>")
def get_entry(category_name, situation_name):
    if category_name not in content:
        abort(404)
    if situation_name not in content[category_name]:
        abort(404)
    return jsonify(content[category_name][situation_name])


@app.route("/category/<category_name>")
def show_category(category_name):
    if category_name not in content:
        abort(404)
    situations = list(content[category_name].keys())
    return render_template(
        "situations.html", category=category_name, situations=situations
    )

@app.route("/category/<category_name>/<situation_name>")
def show_entry(category_name, situation_name):
    if category_name not in content:
        abort(404)
    if situation_name not in content[category_name]:
        abort(404)
    entry = content[category_name][situation_name]
    songs = entry.get("songs", [])
    song = random.choice(songs) if songs else None
    return render_template(
        "entry.html",
        category=category_name,
        situation=situation_name,
        entry=entry,
        song=song,
    )

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)