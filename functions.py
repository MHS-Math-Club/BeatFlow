from flask import render_template, redirect, request
from main import app
import config
import base64
import os
import random as rand
import string as string
import requests
import time
import logging
import json


def createStateKey(size):
	return ''.join(rand.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(size))


def getToken(code):
	token_url = 'https://accounts.spotify.com/api/token'
	redirect_uri = app.config['REDIRECT_URI']
	authorization = app.config['AUTHORIZATION']

	headers = {"Authorization": "Basic {}".format(authorization), 'Accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}

	body = {'code': code, 'redirect_uri': redirect_uri, 'grant_type': 'authorization_code'}
	post_response = requests.post(token_url, headers=headers, data=body)

	# 200 code indicates access token was properly granted
	if post_response.status_code == 200:
		json = post_response.json()
		return json['access_token'], json['refresh_token'], json['expires_in']
	else:
		return None


def refreshToken(refresh_token):
	token_url = 'https://accounts.spotify.com/api/token'
	authorization = app.config['AUTHORIZATION']

	headers = {"Authorization": "Basic {}".format(authorization), 'Content-Type': 'application/x-www-form-urlencoded'}
	body = {'refresh_token': refresh_token, 'grant_type': 'refresh_token'}

	post_response = requests.post(token_url, headers=headers, data=body)

	# 200 code indicates access token was properly granted
	if post_response.status_code == 200:
		return post_response.json()['access_token'], post_response.json()['expires_in']
	else:
		logging.error('refreshToken:' + str(post_response.status_code))
		return None


def checkTokenStatus(session):
	if time.time() > session['token_expiration']:
		payload = refreshToken(session['refresh_token'])

		if payload != None:
			session['token'] = payload[0]
			session['token_expiration'] = time.time() + payload[1]
		else:
			logging.error('checkTokenStatus')
			return None

	return "Success"


def makeGetRequest(session, url, params={}):
	headers = {"Authorization": "Bearer {}".format(session['token'])}
	response = requests.get(url, headers=headers, params=params)	

	if response.status_code == 429:
		if 'Retry-After' in response.headers:
			retry_after = int(response.headers['Retry-After'])
			print(f"Received 429 status code. Waiting for {retry_after} seconds...")
			time.sleep(retry_after)
			# Retry the request
			return makeGetRequest(session, url, params)
		else:
			# Retry immediately without a specified wait time
			print("Received 429 status code without a Retry-After header. Retrying immediately...")
			return makeGetRequest(session, url, params)
	# 200 code indicates request was successful
	if response.status_code == 200:
		return response.json()

	# if a 401 error occurs, update the access token
	elif response.status_code == 401 and checkTokenStatus(session) != None:
		return makeGetRequest(session, url, params)
	else:
		logging.error('makeGetRequest:' + str(response.status_code))
		return None


def makePutRequest(session, url, params={}, data={}):
	headers = {"Authorization": "Bearer {}".format(session['token']), 'Accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
	response = requests.put(url, headers=headers, params=params, data=data)

	# if request succeeds or specific errors occured, status code is returned
	if response.status_code == 204 or response.status_code == 403 or response.status_code == 404 or response.status_code == 500:
		return response.status_code

	# if a 401 error occurs, update the access token
	elif response.status_code == 401 and checkTokenStatus(session) != None:
		return makePutRequest(session, url, data)
	else:
		logging.error('makePutRequest:' + str(response.status_code))
		return None


def makePostRequest(session, url, data):

	headers = {"Authorization": "Bearer {}".format(session['token']), 'Accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
	response = requests.post(url, headers=headers, data=data)

	print(response.content)

	# both 201 and 204 indicate success, however only 201 responses have body information
	if response.status_code == 201:
		return response.json()
	if response.status_code == 204:
		return response

	# if a 401 error occurs, update the access token
	elif response.status_code == 401 and checkTokenStatus(session) != None:
		return makePostRequest(session, url, data)
	elif response.status_code == 403 or response.status_code == 404:
		return response.status_code
	else:
		logging.error('makePostRequest:' + str(response.status_code))
		return None


def makeDeleteRequest(session, url, data):
	headers = {"Authorization": "Bearer {}".format(session['token']), 'Accept': 'application/json', 'Content-Type': 'application/json'}
	response = requests.delete(url, headers=headers, data=data)

	# 200 code indicates request was successful
	if response.status_code == 200:
		return response.json()

	# if a 401 error occurs, update the access token
	elif response.status_code == 401 and checkTokenStatus(session) != None:
		return makeDeleteRequest(session, url, data)
	else:
		logging.error('makeDeleteRequest:' + str(response.status_code))
		return None


def getUserInformation(session):
	url = 'https://api.spotify.com/v1/me'
	payload = makeGetRequest(session, url)

	if payload == None:
		return None

	return payload


def getUserDevices(session):
	url = 'https://api.spotify.com/v1/me/player/devices'
	payload = makeGetRequest(session, url)

	if payload == None:
		return None

	device_list = []
	for device in payload['devices']:

		# restricted devices cannot be accessed by the application
		if device['is_restricted'] != True:
			device_list.append([device['name'], device['id']])

	return device_list


def startPlayback(session, device):
	url = 'https://api.spotify.com/v1/me/player/play'
	params = {'device_id': device}
	payload = makePutRequest(session, url, params)
	return payload


def startPlaybackContext(session, playlist, device):
	url = 'https://api.spotify.com/v1/me/player/play'
	params = {'device_id': device}
	data = "{\"context_uri\":\"" + playlist + "\",\"offset\":{\"position\":0},\"position_ms\":0}"
	payload = makePutRequest(session, url, params, data)
	return payload


def pausePlayback(session):
	url = 'https://api.spotify.com/v1/me/player/pause'
	payload = makePutRequest(session, url)
	return payload


def skipTrack(session):
    url = 'https://api.spotify.com/v1/me/player/next'
    data = {}
    payload = makePostRequest(session, url, data)
    return payload

def addToQueue(session, track_id):
	url = f'https://api.spotify.com/v1/me/player/queue?uri=spotify:track:{track_id}'
	data = {}
	payload = makePostRequest(session, url, data)
	return payload

def playTrack(session, track_id, device):
	addToQueue(session, track_id)
	skipTrack(session)
	startPlayback(session, device)

def getAudioFeatures(session, track_id):
	url = f"https://api.spotify.com/v1/audio-features/{track_id}"
	data = {}
	payload = makeGetRequest(session, url)
	return payload

def getTracks(session, playlist_id, ifWritetoFile):
	url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
	playlist_data = makeGetRequest(session, url)
	tracks_info = []

	for item in playlist_data['tracks']['items']:
		track_id = item['track']['id']

		endpoint = f"https://api.spotify.com/v1/audio-features/{track_id}"
		audio_features = makeGetRequest(session, endpoint)

		track_url = f"https://api.spotify.com/v1/tracks/{track_id}"
		track = makeGetRequest(session, track_url)

		artist_names = [artist['name'] for artist in track['artists']]

		
		track_info = {
			'name': track['name'],
			'artists': artist_names,
			'id': track_id,
			'album': track['album']['name'],
			'duration': track['duration_ms'],
			'image': track['album']['images'][0]['url'],
			'tempo': audio_features['tempo'],
			'time_signature': audio_features['time_signature'],
			'energy': audio_features['energy'],
			'happiness': audio_features['valence'],
			'loudness': audio_features['loudness'],
			'danceability': audio_features['danceability']
		}   
			
		tracks_info.append(track_info)
	if (ifWritetoFile):
		data = sorted(tracks_info, key=lambda x: x['energy'])

		# Convert the list of dictionaries to a JSON string
		json_string = json.dumps(data, indent=4)

		# Write the JSON string to a file
		with open(f"static/data/{playlist_id}.json", "w") as json_file:
			json_file.write(json_string)
	return tracks_info