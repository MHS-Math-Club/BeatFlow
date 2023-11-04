import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

cid = '09d0ffca344548a5931c017a88cddda9'
secret = 'ae66f254352447059ad0ecf5ffa268e8'

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

urn = 'spotify:artist:3jOstUTkEu2JkjvRdBA5Gu'

artist = sp.artist(urn)
print(artist)

user = sp.user('plamere')
print(user)