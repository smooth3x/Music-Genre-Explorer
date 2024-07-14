import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_get_genres():
    response = client.get("/v1/genres")
    assert response.status_code == 200
    json_response = response.json()
    assert any(genre["Genre"].lower() == "rock" for genre in json_response)
    assert any(genre["Genre"].lower() == "pop" for genre in json_response)

def test_get_genre_artists():
    genre_name = "rock"
    response = client.get(f"/v1/genre/{genre_name}")
    assert response.status_code == 200
    json_response = response.json()
    assert "bands" in json_response
    assert "spotify_playlist" in json_response

def test_get_genres_by_artist():
    artist_name = "עומר אדם"  # Omer Adam
    response = client.get(f"/v1/genres_by_artist/{artist_name}")
    assert response.status_code == 200
    json_response = response.json()
    assert "mizrahi" in [genre.lower() for genre in json_response]
