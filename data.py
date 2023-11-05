import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

cid = '09d0ffca344548a5931c017a88cddda9'
secret = 'ae66f254352447059ad0ecf5ffa268e8'

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_tracks_with_info(playlist_id):
    playlist_data = sp.playlist_tracks(playlist_id, limit=100)
    tracks_info = []

    for item in playlist_data['items']:
        track = item['track']
        track_id = track['id']
        tracks_info.append(track_id)

    # Save the track IDs to a text file
    with open('static/data/edm.txt', 'w') as file:
        for track_id in tracks_info:
            file.write(track_id + '\n')

# Replace 'your_playlist_id' with the actual playlist ID you want to retrieve
get_tracks_with_info('3X32dduNQRkqAaYXz0DXHX')
