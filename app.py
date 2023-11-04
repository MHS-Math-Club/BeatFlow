import json
import requests
from flask import Flask, render_template, request, redirect, session, make_response, url_for
from config import Config
from functions import createStateKey, getToken, refreshToken, checkTokenStatus, getUserInformation, getUserDevices, startPlayback, makePostRequest, playTrack
import time

app = Flask(__name__)
app.config.from_object(Config)

app.secret_key = "something"

@app.route("/", methods=["GET", "POST"])
def index():
    if 'user_id' in session:
        device_id = getUserDevices(session)[0][1]
        playTrack(session, '3pv7Q5v2dpdefwdWIvE7yH', device_id)
    else:
        return redirect(url_for('auth'))

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
    client_id = app.config['CLIENT_ID']
    client_secret = app.config['CLIENT_SECRET']
    redirect_uri = app.config['REDIRECT_URI']
    scope = app.config['SCOPE']

    state_key = createStateKey(15)
    session['state_key'] = state_key

    authorize_url = 'https://accounts.spotify.com/en/authorize?'
    parameters = 'response_type=code&client_id=' + client_id + '&redirect_uri=' + redirect_uri + '&scope=' + scope + '&state=' + state_key
    response = make_response(redirect(authorize_url + parameters))

    return response

@app.route('/callback')
def callback():
    code = request.args['code']
    session.pop('state_key', None)

    payload = getToken(code, app)

    if payload != None:
        session['token'] = payload[0]
        session['refresh_token'] = payload[1]
        session['token_expiration'] = time.time() + payload[2]

    current_user = getUserInformation(session)
    session['user_id'] = current_user['id']

    return redirect(url_for('index')) 


