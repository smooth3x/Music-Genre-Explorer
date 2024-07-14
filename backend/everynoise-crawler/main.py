from fastapi import FastAPI, Depends
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from functools import lru_cache
from langdetect import detect

app = FastAPI()

@lru_cache(maxsize=128)
def crawl_genres():
    url = 'https://everynoise.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    genre_items = soup.find_all('div', class_='genre scanme')
    
    genres_data = []
    for item in genre_items:
        genre_name = item.text.strip()[:-1]  # Remove the last character (arrow)
        song_example = item['title'].replace('e.g. ', '') if 'title' in item.attrs else 'N/A'
        preview_url = item['preview_url'] if 'preview_url' in item.attrs else 'N/A'
        
        genres_data.append({
            'Genre': genre_name,
            'Song Example': song_example,
            'Audio Preview': preview_url
        })
    
    return genres_data

@lru_cache(maxsize=128)
def crawl_genre_artists(genre_name):
    cleaned_genre_name = re.sub(r'[^a-zA-Z]', '', genre_name).lower()
    genre_url = f"https://everynoise.com/engenremap-{cleaned_genre_name}.html"
    response = requests.get(genre_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    artists_items = soup.find_all('div', class_='genre scanme')
    
    artists_data = []
    for item in artists_items:
        artists_name = item.text.strip()[:-1]
        song_example = item['title'].replace('e.g. ', '') if 'title' in item.attrs else 'N/A'
        
        # Extract only the song name (YYYY) from the format XXXX - "YYYY"
        if ' "' in song_example:
            song_example = song_example.split(' "')[1].strip('"')
        
        preview_url = item['preview_url'] if 'preview_url' in item.attrs else 'N/A'
        
        artists_data.append({
            'Artist': artists_name,
            'Song Example': song_example,
            'Audio Preview': preview_url
        })
    
    # Fetch Spotify playlist URL
    playlist_url = None
    playlist_url_response = requests.get(f"https://everynoise.com/everynoise1d-{cleaned_genre_name}.html")
    playlist_soup = BeautifulSoup(playlist_url_response.content, 'html.parser')
    playlist_url = extract_spotify_playlist(playlist_soup)

    return {
        'bands': artists_data,
        'spotify_playlist': playlist_url
    }

@lru_cache(maxsize=128)
def crawl_artist_genres(artist):
    # Detect if the artist name is in Hebrew
    if detect(artist) == 'he':
        artist = get_artist_english_name_from_google(artist)
        if not artist:
            return ["Artist not found"]
    
    # Replace spaces with + to correctly format the URL
    artist = artist.replace(' ', '+')

    url = f"https://everynoise.com/lookup.cgi?who={artist}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    response = requests.get(url, headers=headers)
    # Perform the web scraping for artist genres
    soup = BeautifulSoup(response.content, 'html.parser')
    a_tags = soup.find_all('a')
    genres = [tag.text for tag in a_tags]
    
    if genres:
        genres.pop()
    
    return genres

def extract_spotify_playlist(soup):
    iframe_tag = soup.find('iframe', src=re.compile(r'^https://embed.spotify.com'))
    if iframe_tag:
        src = iframe_tag.get('src')
        playlist_id_match = re.search(r'playlist:([a-zA-Z0-9]+)', src)
        if playlist_id_match:
            return playlist_id_match.group(1)
    return None

def get_artist_english_name_from_google(artist_name):
    search_query = f"{artist_name} site:open.spotify.com/artist/"
    search_url = f"https://www.google.com/search?q={search_query}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    response = requests.get(search_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the title of the first result
        first_result = soup.find('h3')
        if first_result:
            return first_result.text
    
    return None

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/v1/genres")
def get_genres():
    genres_data = crawl_genres()
    return genres_data

@app.get("/v1/genre/{genre_name}")
def get_genre_artists(genre_name: str):
    artists_data = crawl_genre_artists(genre_name)
    return artists_data

@app.get("/v1/genres_by_artist/{artist}")
def get_genres_by_artist(artist: str):
    genres = crawl_artist_genres(artist)
    return genres