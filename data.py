import json
import spotipy
import requests
from spotipy.oauth2 import SpotifyClientCredentials
from main import app

cid = '09d0ffca344548a5931c017a88cddda9'
secret = 'ae66f254352447059ad0ecf5ffa268e8'

access_token = "BQDtiYPldcSKfQ3nJ1bKgqPWEs8eIOC5eFYTPaFHuq7WaktpZD4EMafbFVpdWkQTWzAgVLELre4EhAxA5HEQEWOj7azcxl8qGVW5Z24BPU7Is24euNc" # Replace with your Spotify access token

# Set the headers with the access token
headers = {
    "Authorization": f"Bearer {access_token}"
}

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_tracks_with_info(playlist_id):
    """
    Retrieve a list of tracks from a playlist with their name, artist names, ID, album, image URL, and tempo.

    Args:
        playlist_id (str): The unique identifier of the playlist.

    Returns:
        list: A list of dictionaries containing track information, including name, artist names,
              ID, album, image URL, and tempo.
    """
    playlist_data = sp.playlist_tracks(playlist_id, limit=100)
    tracks_info = []

    for item in playlist_data['items']:
        track_id = item['track']['id']
        track = sp.track(track_id)

        endpoint = f"https://api.spotify.com/v1/audio-features/{track_id}"
        response = requests.get(endpoint, headers=headers)
        dance_features = response.json()

        artist_names = [artist['name'] for artist in track['artists']]

        
        track_info = {
            'name': track['name'],
            'artists': artist_names,
            'id': track_id,
            'album': track['album']['name'],
            'duration': int(track['duration_ms'] / 1000),
            'image': track['album']['images'][0]['url'],
            'tempo': dance_features['tempo'],
            'time_signature': dance_features['time_signature'],
            'energy': dance_features['energy'],
            'happiness': dance_features['valence'],
            'loudness': dance_features['loudness'],
            'danceability': dance_features['danceability']
        }   
            
        tracks_info.append(track_info)
    
    return tracks_info

data0 = sorted(get_tracks_with_info("5x9vo8Qya9WpXc9bmf2s3a"), key=lambda x: x['energy'])
data1 = sorted(get_tracks_with_info("2vD8cw6yYjtn2qewxBaJgj"), key=lambda x: x['energy'])
data2 = sorted(get_tracks_with_info("3X32dduNQRkqAaYXz0DXHX"), key=lambda x: x['energy'])
data3 = sorted(get_tracks_with_info("4IAndRau2rqC9men6MMDGr"), key=lambda x: x['energy'])

# Convert the list of dictionaries to a JSON string
json_string0 = json.dumps(data0, indent=4)
json_string1 = json.dumps(data1, indent=4)
json_string2 = json.dumps(data2, indent=4)
json_string3 = json.dumps(data3, indent=4)

# Write the JSON string to a file
with open("static/data/hiphop.json", "w") as json_file:
    json_file.write(json_string0)
with open("static/data/edm.json", "w") as json_file:
    json_file.write(json_string1)
with open("static/data/pop.json", "w") as json_file:
    json_file.write(json_string2)
with open("static/data/classical.json", "w") as json_file:
    json_file.write(json_string3)

print("Data has been written.")
