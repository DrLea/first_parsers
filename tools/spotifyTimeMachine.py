import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

URL = "https://www.billboard.com/charts/hot-100/"
SPOTIFY = "https://api.spotify.com/v1"
ID = ""
SECRET = ""
URI = "https://open.spotify.com/"
USER = ""

scope = "playlist-modify-public"
username = ""
token = SpotifyOAuth(scope=scope, username=username, client_id=ID, client_secret=SECRET, redirect_uri=URI)
spotify = spotipy.Spotify(auth_manager=token)

date = input("yyyy-mm-dd: ") 

response = requests.get(URL+date+"/")
response.raise_for_status()
data = response.text
soup = BeautifulSoup(data, "html.parser")



playlist = []
listOfSongs = []

block = ["Imprint/Promotion Label:","Producer(s):","Songwriter(s):","Have a Tip?","Follow Us","The Daily"]

songs = soup.find_all(name="h3", id="title-of-a-story")
for line in songs:
    line = line.text.strip()
    if line in block:
        pass
    else: 
        playlist.append(line)

for i in playlist:
    try:
        result = spotify.search(q=i)
        listOfSongs.append(result["tracks"]["items"][0]["uri"])
    except:
        pass


spotify.user_playlist_create(user=USER, public=True,name=f"TimeMachine {date}",description="100 songs from past")

preplay = spotify.user_playlists(user=USER)
id = preplay["items"][0]["id"]

listOfSongs = listOfSongs[0:100]
spotify.user_playlist_add_tracks(user=USER, playlist_id=id, tracks=listOfSongs)