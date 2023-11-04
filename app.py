import json
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    playlist = []
    genre = "classical"

    if request.method == "POST":
        genre = request.form.get('genre')

    file_path = f'static/data/{genre}.json'

    with open(file_path, 'r') as json_file:
        playlist = json.load(json_file)

    print(playlist)

    return render_template("index.html", playlist=playlist, genre=genre)
