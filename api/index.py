import os
from api.utils.helpers import *
from flask import Flask, render_template, request, redirect, make_response, url_for
from flask_pymongo import PyMongo


CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
HOST_NAME = os.environ.get('HOST_NAME')
APP_SECRET_KEY = os.environ.get('APP_SECRET_KEY')

app = Flask(__name__)
app.secret_key = APP_SECRET_KEY
#pyMongo
#app.config["MONGO_URI"] = "mongodb://localhost:27017/spotifyStatDB"
#mongo = PyMongo(app)


@app.route('/')
def index():
    return render_template('login-screen.jinja2')


@app.route('/callfrom')
def callfrom():
    return redirect(
        f'https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&redirect_uri=http://{HOST_NAME}/login&scope=user-top-read%20user-library-read&response_type=code')


@app.route('/login', methods=['GET'])
def login():
    try:
        code = request.args['code']
    except KeyError:
        return redirect('/callfrom')

    url = 'https://accounts.spotify.com/api/token'
    payload = {
        'grant_type': "authorization_code",
        'code': code,
        'redirect_uri': f'http://{HOST_NAME}/login',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    response = requests.request("POST", url, data=payload)
    response = response.json()

    if response['refresh_token']:
        refresh_token = response['refresh_token']
    access_token = response['access_token']

    resp = make_response(redirect('/dashboard'))
    resp.set_cookie('access_token', access_token)
    return resp


@app.route('/dashboard')
def dashboard():
    access_token = request.cookies.get('access_token')
    if not access_token:
        return redirect('/login')

    url = "https://api.spotify.com/v1/me/top/tracks?time_range=short_term&limit=10&offset=0"
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    numPulls = 15;

    response = requests.request("GET", url, headers=headers)
    short_term_tracks = response.json()

    url = f'https://api.spotify.com/v1/me/top/tracks?time_range=medium_term&limit={numPulls}&offset=0'

    response = requests.request("GET", url, headers=headers)
    medium_term_tracks = response.json()

    url = f'https://api.spotify.com/v1/me/top/tracks?time_range=long_term&limit={numPulls}&offset=0'

    response = requests.request("GET", url, headers=headers)
    long_term_tracks = response.json()

    url = f'https://api.spotify.com/v1/me/top/artists?time_range=short_term&limit={numPulls}&offset=0'

    response = requests.request("GET", url, headers=headers)
    short_term_artists = response.json()

    url = f'https://api.spotify.com/v1/me/top/artists?time_range=medium_term&limit={numPulls}&offset=0'

    response = requests.request("GET", url, headers=headers)
    medium_term_artists = response.json()

    url = f'https://api.spotify.com/v1/me/top/artists?time_range=long_term&limit={numPulls}&offset=0'

    response = requests.request("GET", url, headers=headers)
    long_term_artists = response.json()

    return render_template('dashboard-stats.jinja2', short_term_tracks=short_term_tracks, medium_term_tracks=medium_term_tracks,
                           long_term_tracks=long_term_tracks, short_term_artists=short_term_artists,
                           medium_term_artists=medium_term_artists, long_term_artists=long_term_artists)


@app.route('/rawtext_scale', methods=['GET', 'POST'])
def rawtext_scale():

    access_token = request.cookies.get('access_token')
    if not access_token:
        return redirect('/login')

    url = "https://api.spotify.com/v1/me/top/tracks?time_range=short_term&limit=10&offset=0"
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    BASE_URL = "https://api.spotify.com/v1/me/top"

    response = requests.request("GET", url, headers=headers)
    short_term_tracks = response.json()

    url = f"{BASE_URL}/tracks?time_range=medium_term&limit=10&offset=0"

    response = requests.request("GET", url, headers=headers)
    medium_term_tracks = response.json()

    url = "https://api.spotify.com/v1/me/top/tracks?time_range=long_term&limit=10&offset=0"

    response = requests.request("GET", url, headers=headers)
    long_term_tracks = response.json()

    url = "https://api.spotify.com/v1/me/top/artists?time_range=short_term&limit=10&offset=0"

    response = requests.request("GET", url, headers=headers)
    short_term_artists = response.json()

    url = "https://api.spotify.com/v1/me/top/artists?time_range=medium_term&limit=10&offset=0"

    response = requests.request("GET", url, headers=headers)
    medium_term_artists = response.json()

    url = "https://api.spotify.com/v1/me/top/artists?time_range=long_term&limit=10&offset=0"

    response = requests.request("GET", url, headers=headers)
    long_term_artists = response.json()

    if not short_term_tracks:
        return redirect(url_for('login'))

    return render_template('raw_text_output.jinja2', short_term_tracks=short_term_tracks, medium_term_tracks=medium_term_tracks,
                           long_term_tracks=long_term_tracks, short_term_artists=short_term_artists,
                           medium_term_artists=medium_term_artists, long_term_artists=long_term_artists)

@app.route('/recent_listening_analysis')
def recent_listening_analysis():

    access_token = request.cookies.get('access_token')
    if not access_token:
        return redirect('/login')

    url = "https://api.spotify.com/v1/me/top/tracks?time_range=short_term&limit=50&offset=0"
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("GET", url, headers=headers)
    short_track_ids = pullIds(response.json())

    recent_audio_features = getPlaylistStatsJson(short_track_ids, access_token)

    return render_template('recent_listening_analysis.jinja2', recent_audio_features=recent_audio_features)

if __name__ == "__main__":
    app.run(debug=True)
