import requests


# takes in a dict of songs and returns a list of their id's
def pullIds(songs):
    return [song['id'] for song in songs['items']]


# takes in a list of song ID's, returns a dictionary of their average stats
def getPlaylistStatsJson(songs, access_token):
    short_track_ids = '%2C'.join(songs)

    url = f'https://api.spotify.com/v1/audio-features?ids={short_track_ids}'
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.request("GET", url, headers=headers)
    recent_audio_features_all = response.json()['audio_features']

    num_songs = len(recent_audio_features_all)

    avg_audio_features = {
        "acousticness" : 0,
        "danceability" : 0,
        "duration_ms" : 0,
        "energy" : 0,
        "instrumentalness" : 0,
        "liveness" : 0,
        "loudness" : 0,
        "speechiness" : 0,
        "tempo": 0,
        "valence" : 0,
    }

    for song in recent_audio_features_all:
        for key, value in avg_audio_features.items():
            avg_audio_features[key] += song[key]

    for key, value in avg_audio_features.items():
        avg_audio_features[key] /= num_songs

    return avg_audio_features
