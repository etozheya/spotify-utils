import requests

SPOTIFY_URL = 'https://api.spotify.com/v1/'


def get_headers(jwt):
    return {'Authorization': f'Bearer {jwt}'}


def list_playlists(jwt, user_id=None):
    if user_id:
        url = SPOTIFY_URL + f'users/{user_id}/playlists'
    else:
        url = SPOTIFY_URL + 'me/playlists'
    resp = requests.get(url, headers=get_headers(jwt))
    return resp.json()


def list_tracks(jwt, playlist_id):
    url = SPOTIFY_URL + f'playlists/{playlist_id}/tracks'
    headers = get_headers(jwt)
    all_tracks = []
    limit = 50
    offset = 0

    while True:
        params = {'limit': limit, 'offset': offset}
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        tracks = data.get("items", [])
        all_tracks.extend(tracks)
        if len(tracks) < limit:
            break
        offset += limit

    return all_tracks


def create_playlist(jwt, user_id, name, public=False):
    url = SPOTIFY_URL + f'users/{user_id}/playlists'
    payload = {
        'name': name,
        'description': 'reversed playlist',
        'public': public}
    resp = requests.post(url, headers=get_headers(jwt), json=payload)
    return resp.json()


def add_tracks_to_playlist(jwt, playlist_id, track_ids):
    url = SPOTIFY_URL + f'playlists/{playlist_id}/tracks'
    payload = {'uris': [f'spotify:track:{tid}' for tid in track_ids]}
    requests.post(url, headers=get_headers(jwt), json=payload)


def get_playlist_name(jwt, playlist_id):
    url = SPOTIFY_URL + f'playlists/{playlist_id}'
    resp = requests.get(url, headers=get_headers(jwt))
    if resp.status_code == 200:
        return resp.json()['name']
    return ''
