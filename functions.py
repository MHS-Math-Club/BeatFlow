from flask import render_template, redirect, request
import config
import base64
import os
import random as rand
import string as string
import requests
import time
import logging


"""
AUTHENTICATION: To make a request to the Spotify API, the application needs an access
token for the user. This token expires every 60 minutes. To acquire a new token, the 
refresh token can be sent to the API, which will return a new access token.
"""

"""
Creates a state key for the authorization request. State keys are used to make sure that
a response comes from the same place where the initial request was sent. This prevents attacks,
such as forgery. 
Returns: A state key (str) with a parameter specified size.
"""
def createStateKey(size):
	#https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits
	return ''.join(rand.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(size))


"""
Requests an access token from the Spotify API. Only called if no refresh token for the
current user exists.
Returns: either [access token, refresh token, expiration time] or None if request failed
"""
def getToken(code, app):
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


"""
Requests an access token from the Spotify API with a refresh token. Only called if an access
token and refresh token were previously acquired.
Returns: either [access token, expiration time] or None if request failed
"""
def refreshToken(refresh_token, app):
	token_url = 'https://accounts.spotify.com/api/token'
	authorization = app.config['AUTHORIZATION']

	headers = {'Authorization': authorization, 'Accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
	body = {'refresh_token': refresh_token, 'grant_type': 'refresh_token'}
	post_response = requests.post(token_url, headers=headers, data=body)

	# 200 code indicates access token was properly granted
	if post_response.status_code == 200:
		return post_response.json()['access_token'], post_response.json()['expires_in']
	else:
		logging.error('refreshToken:' + str(post_response.status_code))
		return None

"""
Determines whether new access token has to be requested because time has expired on the 
old token. If the access token has expired, the token refresh function is called. 
Returns: None if error occured or 'Success' string if access token is okay
"""
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

"""
REQUESTS: Functions to make GET, POST, PUT, and DELETE requests with the correct
authorization headers.
"""

"""
Makes a GET request with the proper headers. If the request succeeds, the json parsed
response is returned. If the request fails because the access token has expired, the
check token function is called to update the access token.
Returns: Parsed json response if request succeeds or None if request fails
"""
def makeGetRequest(session, url, params={}):
	headers = {"Authorization": "Bearer {}".format(session['token'])}
	response = requests.get(url, headers=headers, params=params)

	# 200 code indicates request was successful
	if response.status_code == 200:
		return response.json()

	# if a 401 error occurs, update the access token
	elif response.status_code == 401 and checkTokenStatus(session) != None:
		return makeGetRequest(session, url, params)
	else:
		logging.error('makeGetRequest:' + str(response.status_code))
		return None


"""
Makes a PUT request with the proper headers. If the request succeeds or specific errors
occured, the status code is returned. The status code is necessary to identify some errors
that need to be brought to the user's attention (inactive device and forbidden requests due
to Spotify Premium. If the request fails because the access token has expired, the
check token function is called to update the access token.
Returns: Response status code if request succeeds or None if request fails
"""
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

"""
Makes a POST request with the proper headers. If the request succeeds, the json parsed
response is returned. If the request fails because the access token has expired, the
check token function is called to update the access token. If the requests fails
due to inactive devices or forbidden requests the status code is returned.
Returns: Parsed json response if request succeeds or None/status code if request fails
"""
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

"""
Makes a DELETE request with the proper headers. If the request succeeds, the json parsed
response is returned. If the request fails because the access token has expired, the
check token function is called to update the access token.
Returns: Parsed json response if request succeeds or None if request fails
"""
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

"""
PERSONAL USER INFORMATION: Functions that get information specific to the user.
"""

"""
Gets user information such as username, user ID, and user location.
Returns: Json response of user information
"""
def getUserInformation(session):
	url = 'https://api.spotify.com/v1/me'
	payload = makeGetRequest(session, url)

	if payload == None:
		return None

	return payload

"""
PLAYBACK: Functions that alter a user's playback or get information about playback.
"""

"""
Gets all of a user's available devices.
Returns: A list of devices, which are a list of [name, id]
"""
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


"""
Start a user's playback from the current context and parameter specified device.
Returns: The response of the start request (for 403/404 error processing)
"""
def startPlayback(session, device):
	url = 'https://api.spotify.com/v1/me/player/play'
	params = {'device_id': device}
	payload = makePutRequest(session, url, params)
	return payload


"""
Start a user's playback from the parameter specified context and device.
Returns: The response of the start request (for 403/404 error processing)
"""
def startPlaybackContext(session, playlist, device):
	url = 'https://api.spotify.com/v1/me/player/play'
	params = {'device_id': device}
	data = "{\"context_uri\":\"" + playlist + "\",\"offset\":{\"position\":0},\"position_ms\":0}"
	payload = makePutRequest(session, url, params, data)
	return payload


"""
Pauses a user's playback.
Returns: The response of the start request (for 403/404 error processing)
"""
def pausePlayback(session):
	url = 'https://api.spotify.com/v1/me/player/pause'
	payload = makePutRequest(session, url)
	return payload


"""
Skips to the next track in a user's playback from the current context.
Returns: The response of the start request (for 403/404 error processing)
"""
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
	pausePlayback(session)
	addToQueue(session, track_id)
	skipTrack(session)
	startPlayback(session, device)
