from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", song_name="Shake it Off", album_name="1989", artist_name="david", id="art")
