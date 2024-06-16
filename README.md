<h1 align="center">
<img src="https://i.ibb.co/9ynJnTh/logo.png" alt="Music Genre Explorer" width="800">
</h1>

<h4 align="center">A simple platform for searching and discovering music genres using <a href="http://everynoise.com" target="_blank">Everynoise.com</a>.</h4>

<p align="center">
  <img src="https://img.shields.io/badge/-Python-yellow?style=for-the-badge&logo=Python&logoColor=white">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi">
  <img src="https://img.shields.io/badge/-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white">
</p>

<p align="center">
  <a href="#About">About</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#installation">Installation</a> •
  <a href="#credits">Credits</a> •
</p>

## About

Music Genre Explorer is a web application designed to facilitate exploration of over 6000 genres of music, enabling users to discover new artists and musical styles. <br />
It uses web scraping to fetch genre data from [EveryNoise](https://everynoise.com/) and provides a simple API to access this data.

## How To Use

- Searching Genres:
  - You can search and select a genre from the genre list.
    - <img src="https://pouch.jumpshare.com/preview/-bRXRDGJ1QivZi_hCLz4LRTRTgubiC3WYm0BK7yhaAqaDA69EaFpivcEq9hyK_hxt4eIeRAytGBN7ouYLN-ePsGv3oxlRWXwN0RlZ6Ir9Ug" style="text-align: left;">
  - Or, you can search genres by artist name.
    - <img src="https://pouch.jumpshare.com/preview/Pbaqp6fkBAoIXayIlgB4WO42jWS3Z2ztAnJ5DLaz7bcxU3-iZHQx19hQNMjiuEift4eIeRAytGBN7ouYLN-ePpAZFgxNutZEWoBfLrVWebA" style="text-align: left;">
- Exploring Genres:
  - Each genre will present its most popular artists, previews of their songs, and a spotify list so you can save them for later.

## Installation

To clone and run this application, you'll need [Git](https://git-scm.com) and [Docker](https://www.docker.com/products/docker-desktop/). From your command line:

```bash
# Clone this repository
$ git clone https://github.com/smooth3x/Music-Genre-Explorer

# Go into the repository
$ cd Music-Genre-Explorer

# Build the docker-compose file
$ docker-compose build

# Run the app
$ docker-compose up
```

## Credits

This application couldn't be completed without the data from [EveryNoise](https://everynoise.com)
