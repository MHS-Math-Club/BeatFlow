import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

cid = '09d0ffca344548a5931c017a88cddda9'
secret = 'ae66f254352447059ad0ecf5ffa268e8'

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


#gets list of tracks with name of track, artist names, id, album, image (as url)
def getTracks(playlistId):
    playlist = sp.playlist_tracks(playlistId, limit=100)
    tracks = []

    id = playlist['items'][0]['track']['id']
    track = sp.track(id)

    for i in range(len(playlist['items'])):
        id = playlist['items'][i]['track']['id']
        track = sp.track(id)
        names = []
        for j in range(len(track['artists'])):
            names.append(track['artists'][j]['name'])
        Dict = {'name': track['name'], 'artists': names, 'id': id, 'album': track['album']['name'], 'image': track['album']['images'][0]['url']}
        tracks.append(Dict)
    return tracks