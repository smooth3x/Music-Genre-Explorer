from bs4 import BeautifulSoup
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
import requests
import re
import json

app = FastAPI()

def get_access_token():
    response = requests.get("https://open.spotify.com/get_access_token?reason=transport&productType=web_player")
    data = response.json()
    return data["accessToken"]

def fetch_all_spotify_genres():
    access_token = get_access_token()
    headers = {
      "Authorization": f"Bearer {access_token}"
    }
    url = f"https://api.spotify.com/v1/users/thesoundsofspotify/playlists"
    playlist_data = []

    while url:
        response = requests.get(url, headers=headers)
        data = response.json()
        for item in data["items"]:
            # Extract genre using regex (assuming "The Sound of" format)
            match = re.search(r"The Sound of ((?!Everything).+)", item["name"], flags=re.IGNORECASE)
            if match:
                genre = match.group(1)
                genre_playlist_id = item["id"]
                top_song_info = get_top_song(access_token, genre_playlist_id)
                playlist_data.append({
                    "genre": genre,
                    "genre_playlist_id": genre_playlist_id,
                    **top_song_info  # Unpack top song info dictionary
                })
        url = data["next"] if data["next"] else None
    return playlist_data

def fetch_all_genres_from_everynoise():
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
            'genre_name': genre_name,
            'top_track_name': song_example,
            'top_track_audio_url': preview_url
        })

    # Save the genres_data to a JSON file
    with open('spotify_genres.json', 'w', encoding='utf-8') as f:
        json.dump(genres_data, f, ensure_ascii=False, indent=4)

def fetch_genres_by_artist(artist_name):
    access_token = get_access_token()
    artist = search_artist(access_token, artist_name)
    genres = artist["genres"]

    return genres

def get_top_song(access_token, playlist_id):
    access_token = get_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit=1"
    response = requests.get(url, headers=headers)
    data = response.json()
    
    # Assuming the first track is the most popular (adjust logic if needed)
    if data["items"]:
        top_track = data["items"][0]["track"]
        artists = ", ".join([artist["name"] for artist in top_track["artists"]])
        preview_url = top_track.get("preview_url")  # Preview URL might be None

        return {
            "top_song_id": top_track["id"],
            "top_song_artist": artists,
            "top_song_name": top_track["name"],
            "top_song_audio_url": preview_url
        }
    else:
        return {
            "top_song_id": "No songs found",
            "top_song_artist": "No songs found",
            "top_song_name": "No songs found",
            "top_song_audio_url": None
        }

def get_track(access_token, track_id):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    response = requests.get(url, headers=headers)
    data = response.json()

    if data is not None:
        artists = ", ".join([artist["name"] for artist in data["artists"]])

        return {
            "top_song_id": data["id"],
            "top_song_artist": artists,
            "top_song_name": data["name"],
            "top_song_audio_url": data["preview_url"]
        }
    
    return None

def search_artist(access_token, artist_name):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    params = {
        "q": artist_name,
        "type": "artist"
    }

    response = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)
    data = response.json()

    return data["artists"]["items"][0]

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/v1/spotify-search/{query}")
def spotify_search_artists(query: str):
    access_token = get_access_token()
    artist = search_artist(access_token, query)
    return artist

@app.get("/v1/spotify-genres")
def spotify_get_all_genres():
    genres_data = fetch_all_spotify_genres()

    if 'error' in genres_data:
        return JSONResponse(status_code=genres_data['error']['status'], content=genres_data['error'])
    
    with open("spotify_genres.json", "w", encoding='utf-8') as f:
        json.dump(genres_data, f, ensure_ascii=False, indent=4)

    return genres_data

@app.post("/v1/everynoise-genres")
def everynoise_genres():
    fetch_all_genres_from_everynoise()
    return {"message": "Genres updated successfully."}

@app.get("/v1/spotify-playlist-first-song/{playlist_id}")
def spotify_get_first_song(playlist_id: str):
    access_token = get_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit=1"
    response = requests.get(url, headers=headers)
    data = response.json()
    return data

@app.get("/v1/spotify-artist-genres/{artist_name}")
def spotify_get_artist_genres(artist_name: str):
    genres = fetch_genres_by_artist(artist_name)
    return genres

@app.get("/v1/spotify-track/{track_id}")
def spotify_get_track(track_id: str):
    access_token = get_access_token()
    return get_track(access_token, track_id)