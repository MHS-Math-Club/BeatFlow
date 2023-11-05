import requests
import json
from flask import Flask, render_template, request, redirect, session, make_response, url_for
from functions import createStateKey, getToken, refreshToken, checkTokenStatus, getUserInformation, getUserDevices, startPlayback, makePostRequest, playTrack, getTracks
import time
from main import app
from pyngrok import ngrok

app.secret_key = "something"
ngrok.set_auth_token('2Xjeq4GP6viuzqaDO9XrIeg31LX_53i3r6zsfhwkvpy9nMt1K')
public_url = "https://f9da-129-130-19-169.ngrok-free.app"

@app.route("/", methods=["GET", "POST"])
def index():
    if 'user_id' in session:
        device_id = getUserDevices(session)[0][1]

        genre = 'classical'
        playlist = []
        index = 0

        if request.method == "POST":
            genre = request.form.get('genre')
            # find index of song

        file_path = f'static/data/{genre}.json'

        with open(file_path, 'r') as json_file:
            playlist = json.load(json_file)

        playTrack(session, playlist[index]['id'], device_id)
            
        return render_template("index.html", playlist=playlist, genre=genre, index=index)
    else:
        return redirect(url_for('auth'))

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

    payload = getToken(code)

    if payload != None:
        session['token'] = payload[0]
        session['refresh_token'] = payload[1]
        session['token_expiration'] = time.time() + payload[2]

    current_user = getUserInformation(session)
    session['user_id'] = current_user['id']

    return redirect(url_for('index')) 

if __name__ == '__main__':
    app.run(port=5003, debug=True)


