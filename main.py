from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import requests
import spotipy

load_dotenv()

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"}

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri=os.getenv("REDIRECT_URI"),
        scope="playlist-modify-private",
        show_dialog=True,
        cache_path="token.txt",
        username=os.getenv("USER_NAME")
    )
)
current_user_id = sp.current_user()['id']
users_date = input("Which year do you want to travel to ? Type the date in this format YYYY-MM-DD: ")
year = users_date.split("-")[0]

url = f"https://www.billboard.com/charts/hot-100/{users_date}/"
response = requests.get(url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
song_elements = soup.select(selector="div li ul h3")
songs_name = [song.get_text().strip() for song in song_elements]

song_uris = []
for song in songs_name:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

new_playlist = sp.user_playlist_create(
    user=current_user_id,
    name=f"{users_date} Billboard 100",
    public=False,
    collaborative=False,
    description=''
)

playlist_id = new_playlist["id"]
sp.playlist_add_items(playlist_id=playlist_id, items =song_uris)

































