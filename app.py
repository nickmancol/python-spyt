import os
import json
import spotipy
import pyyoutube
from flasgger import Swagger
from flask_restful import Api, Resource
from flask import Flask, jsonify, request
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)
swagger = Swagger(app)
ytapi = pyyoutube.Api(api_key=os.environ['YT_ID'])

@app.route('/spyt', methods=['GET'])
def get():
    """
        file: spec.yml
    """
    num = int(request.args['num']) if 'num' in request.args else 10
    playlist = request.args['playlist'] if 'playlist' in request.args else '37i9dQZEVXbMDoHDwVN2tF'
    try:
        items = spotify_songs(num, playlist)
    except spotipy.client.SpotifyException as e:
        return jsonify({'Spotify error':e.msg, 'source':'Spotify'}), 500
    except pyyoutube.error.PyYouTubeException as e:
        return jsonify({'error':e.message, 'source':'Youtube'}), 500

    return jsonify(items), 200, {'Content-type':'application/json'}

def spotify_songs(number, playlist):
    items = []
    res = spotipy.Spotify( client_credentials_manager=SpotifyClientCredentials() )
    results = res.playlist( playlist )
    number = min(len(results['tracks']['items']), number)
    
    for track in results['tracks']['items'][:number]:
        artist = track['track']['album']['artists'][0]['name']
        title = track['track']['name']
        r = ytapi.search_by_keywords(q=artist + ' ' + title , search_type=["video"], count=1, limit=1)
        item = {"artist":artist, "title":title}
        for r in r.items:
            item["video"] = {"id":r.id.videoId, "title":r.snippet.title, "desc":r.snippet.description}
        items.append( item )
    return items

if __name__ == "__main__":
    app.run(debug=True)