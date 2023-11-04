import json
from flask import Flask, render_template, request, redirect, session
from spotify_requests import spotify

app = Flask(__name__)
app.secret_key = "something"

@app.route("/", methods=["GET", "POST"])
def index():
    if 'auth_header' in session:
        #

    playlist = []
    genre = "classical"

    if request.method == "POST":
        genre = request.form.get('genre')

    file_path = f'static/data/{genre}.json'

    with open(file_path, 'r') as json_file:
        playlist = json.load(json_file)

    return render_template("index.html", playlist=playlist, genre=genre)

@app.route("/auth")
def auth():
    return redirect(spotify.AUTH_URL)

@app.route('/callback')
def callback():
    auth_token = request.args['code']
    auth_header = spotify.authorize(auth_token)
    session['auth_header'] = auth_header

    return index()

