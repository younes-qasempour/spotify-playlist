from bs4 import BeautifulSoup
from datetime import datetime
import requests

# users_date = input("Which year do you want to travel to ? Type the date in this format YYYY-MM-DD: ")
users_date = "2010-12-03"
url = f"https://www.billboard.com/charts/hot-100/{users_date}/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

response = requests.get(url, headers=headers)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")
song_elements = soup.select(selector="div li ul h3")
songs_name = [song.get_text().strip() for song in song_elements]
