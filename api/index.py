import os
import requests
from flask import Flask, render_template, request, redirect, make_response

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
HOST_NAME = os.environ.get('HOST_NAME')

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/callfrom')
def callfrom():
    return redirect(
        f'https://accounts.spotify.com/authorize?client_id=2387ae6eda67486599124f3f62289867&redirect_uri=http://{HOST_NAME}/login&scope=user-top-read%20user-library-read&response_type=code')


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

    response = requests.request("GET", url, headers=headers, data=payload)
    short_term_tracks = response.json()

    url = "https://api.spotify.com/v1/me/top/tracks?time_range=medium_term&limit=10&offset=0"
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    medium_term_tracks = response.json()

    url = "https://api.spotify.com/v1/me/top/tracks?time_range=long_term&limit=10&offset=0"
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    long_term_tracks = response.json()

    url = "https://api.spotify.com/v1/me/top/artists?time_range=short_term&limit=10&offset=0"
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    short_term_artists = response.json()

    url = "https://api.spotify.com/v1/me/top/artists?time_range=medium_term&limit=10&offset=0"
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    medium_term_artists = response.json()

    url = "https://api.spotify.com/v1/me/top/artists?time_range=long_term&limit=10&offset=0"
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    long_term_artists = response.json()

    print(short_term_artists)
    # return render_template('test.html')
    print(short_term_tracks)
    return render_template('name.jinja2', short_term_tracks=short_term_tracks, medium_term_tracks=medium_term_tracks,
                           long_term_tracks=long_term_tracks, short_term_artists=short_term_artists,
                           medium_term_artists=medium_term_artists, long_term_artists=long_term_artists)


if __name__ == "__main__":
    app.run(debug=True)
