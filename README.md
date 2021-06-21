# Sample microservice implementation

![Flask](https://github.com/github/docs/actions/workflows/flask.yml/badge.svg)

This microservice reads the Spotify top 50 global songs and search the most popular video associated with the song's title in Youtube. Implemented with Nameko framework over HTTP/REST.

## Installing depedencies

```
pip install -r requirements.txt
```

## Config

Please set the following environment variables before running:

```
YT_ID=XXX
SPOTIPY_CLIENT_ID=XXX
SPOTIPY_CLIENT_SECRET=XXX
PLAYLIST_ID=37i9dQZEVXbMDoHDwVN2t
```
## Running 

```
python app.py
```