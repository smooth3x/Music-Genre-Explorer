<h1 align="center">
<img src="https://i.ibb.co/9ynJnTh/logo.png" alt="Music Genre Explorer" width="800">
</h1>

<h4 align="center">A simple platform for searching and discovering music genres using data from <a href="http://everynoise.com">Everynoise.com</a>.</h4>

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/-Python-yellow?style=for-the-badge&logo=Python&logoColor=white"></a>
  <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi"></a>
  <a href="https://streamlit.io/"><img src="https://img.shields.io/badge/-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"></a>
</p>

<p align="center">
  • <a href="#About">About</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#installation">Installation</a> •
  <a href="#credits">Credits</a> •
</p>

## About

• <strong style="color:#FFAF69;">Music Genre Explorer</strong> is a web application designed to facilitate exploration of over <strong style="color:#FFAF69;">6000 genres</strong> of music, enabling users to discover new artists and musical styles. <br />
• It uses web scraping to fetch genre data from [EveryNoise](https://everynoise.com/) and provides a simple API to access this data.

## How To Use

- Searching Genres:
  - You can search and select a genre from the genre list.
    - <img src="https://pouch.jumpshare.com/preview/Y2D5bAdaCqP-_V1u2RnxZyFdu-zWONd2wN7s7KARsUTc-zDCOSjGYF-CWuaKEIxkJtDrGaXPp-rsI8Oxq8guc9P28AAMXVc4ArqCyqfLVPk" style="text-align: left;">
  - Or, you can search genres by artist name.
    - <img src="https://pouch.jumpshare.com/preview/ztUtdj4iCCfpG0Guc5YKDL00gSfH5KHmQUivqq1TukyFKHkHAPdBq5LzBiKakRzoJtDrGaXPp-rsI8Oxq8guc2i9arcvSS0OEjrUYGYLflc" style="text-align: left;">
- Exploring Genres:
  - Each genre will present its most popular artists, previews of their songs, and a spotify list so you can save them for later.

## Installation

To clone and run this application, you'll need [Git](https://git-scm.com) and [Docker](https://www.docker.com/products/docker-desktop/). From your command line:

```bash
# Clone this repository
$ git clone https://github.com/smooth3x/Music-Genre-Explorer

# Go into the repository
$ cd Music-Genre-Explorer

# Build the docker-compose file & Run
$ docker-compose up --build
```

## Credits

This application couldn't be completed without the data from [Everynoise.com](https://everynoise.com)
