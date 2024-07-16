import pytest
from main import crawl_genres, crawl_genre_artists

def test_crawl_genres_contains_rock_and_pop():
    genres_data = crawl_genres()
    genres = [genre_dict['Genre'] for genre_dict in genres_data]
    assert "rock" in genres, "'rock' should be in the genres list"
    assert "pop" in genres, "'pop' should be in the genres list"

def test_crawl_genre_artists_rock_contains_metallica():
    artists_data = crawl_genre_artists("rock")
    artists = [artist_dict['Artist'] for artist_dict in artists_data['bands']]
    assert "Metallica" in artists, "'Metallica' should be in the artists list for 'rock'"
