import base64
import webbrowser
from urllib.parse import urlencode

import requests


def get_jwt(client_id, client_secret, code, redirect_url):
    url = 'https://accounts.spotify.com/api/token'
    credentials = f'{client_id}:{client_secret}'
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_url}
    try:
        resp = requests.post(url, headers=headers, data=payload)
        resp.raise_for_status()
        return resp.json()['access_token']
    except requests.exceptions.HTTPError as e:
        print(f'HTTP Error: {e}')
        if resp.status_code == 401:
            raise ValueError('Invalid client credentials provided.')
        else:
            raise Exception(f'Failed to retrieve access token: {resp.text}')
    except Exception as e:
        raise Exception(f'Unexpected error occurred: {e}')


def authorize(client_id, redirect_url):
    params = {
        'response_type': 'code',
        'client_id': client_id,
        'scope': 'user-library-read playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public',
        'redirect_uri': redirect_url}
    webbrowser.open(
        'https://accounts.spotify.com/authorize?' + urlencode(params))


def get_name(jwt):
    url = 'https://api.spotify.com/v1/me'
    headers = {'Authorization': f'Bearer {jwt}'}
    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()['display_name']
    except requests.exceptions.HTTPError as e:
        print(f'HTTP Error: {e}')
        raise Exception(f'Failed to retrieve user name: {resp.text}')
    except Exception as e:
        raise Exception(f'Unexpected error occurred: {e}')
