from fastapi import FastAPI, Depends
import requests
from bs4 import BeautifulSoup
import re

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/v1/genres")
def get_genres():
    response = requests.get("http://everynoise-crawler:8000/v1/genres")
    return response.json()

@app.get("/v1/genre/{genre_name}")
def get_genre_artists(genre_name: str):
    response = requests.get(f"http://everynoise-crawler:8000/v1/genre/{genre_name.replace(' ', '').lower()}")
    return response.json()

@app.get("/v1/artist-genres/{artist}")
def get_genres_by_artist(artist: str):
    response = requests.get(f"http://spotify-api:8000/v1/spotify-artist-genres/{artist}")
    return response.json()