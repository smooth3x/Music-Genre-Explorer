import pytest
from main import fetch_genres_by_artist

def test_fetch_genres_by_artist():
    genres = fetch_genres_by_artist("Omer Adam")
    assert "mizrahi" in genres, "Expected 'mizrahi' to be in the genres list"
