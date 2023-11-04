import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

cid = '09d0ffca344548a5931c017a88cddda9'
secret = 'ae66f254352447059ad0ecf5ffa268e8'

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_tracks_with_info(playlist_id):
    """
    Retrieve a list of tracks from a playlist with their name, artist names, ID, album, and image URL.

    Args:
        playlist_id (str): The unique identifier of the playlist.

    Returns:
        list: A list of dictionaries containing track information, including name, artist names,
              ID, album, and image URL.
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
            'image': track['album']['images'][0]['url']
        }
        
        tracks_info.append(track_info)
    
    return tracks_info

