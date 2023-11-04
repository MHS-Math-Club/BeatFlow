import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

cid = '09d0ffca344548a5931c017a88cddda9'
secret = 'ae66f254352447059ad0ecf5ffa268e8'

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
        
        artist_names = [artist['name'] for artist in track['artists']]
        
        track_info = {
            'name': track['name'],
            'artists': artist_names,
            'id': track_id,
            'album': track['album']['name'],
            'image': track['album']['images'][0]['url'],
            'tempo':sp.audio_features([track_id])[0]['tempo'],
            'time_signature': sp.audio_features([track_id])[0]['time_signature'],
            'energy': sp.audio_features([track_id])[0]['energy'],
            'happiness': sp.audio_features([track_id])[0]['valence'],
            'loudness': sp.audio_features([track_id])[0]['loudness']
        }
        
        tracks_info.append(track_info)
    
    return tracks_info

data = sorted(get_tracks_with_info("27Zm1P410dPfedsdoO9fqm"), key=lambda x: x['tempo'])

# Convert the list of dictionaries to a JSON string
json_string = json.dumps(data, indent=4)

# Write the JSON string to a file
with open("data.json", "w") as json_file:
    json_file.write(json_string)

print("Data has been written to data.json")