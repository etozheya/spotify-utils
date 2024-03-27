import json

import auth
import spotify


def get_credentials():
    try:
        with open('credentials.json', 'r') as file:
            credentials = json.load(file)
    except FileNotFoundError:
        credentials = {
            'client_id': None, 'client_secret': None, 'redirect_url': None}
    return credentials


def save_credentials(credentials):
    with open('credentials.json', 'w') as file:
        json.dump(credentials, file, indent=4)


def authenticate():
    client_id = input('Enter your client ID: ')
    client_secret = input('Enter your client secret: ')
    redirect_url = input('Enter your redirect url: ')
    save_credentials(
        {
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_url': redirect_url})


def get_jwt_and_username():
    credentials = get_credentials()
    auth.authorize(credentials['client_id'], credentials['redirect_url'])
    code = input(
        'Enter code after `code=` from the URL from the browser: ')
    jwt = auth.get_jwt(credentials['client_id'],
                       credentials['client_secret'], code,
                       credentials['redirect_url'])
    username = auth.get_name(jwt)
    return jwt, username


def main():
    credentials = get_credentials()
    if not credentials.get('client_id') or \
            not credentials.get('client_secret') or \
            not credentials.get('redirect_url'):
        print('Please set your client ID, client secret and redirect url.')
        authenticate()
    jwt, username = get_jwt_and_username()
    print(f'Retrieved JWT: {jwt[:5]} ..')
    print(f'Hello, {username}')
    while True:
        print('\nOptions:')
        print('1. Change user')
        print('2. List your playlists')
        print('3. Reverse a playlist')
        print('4. Exit')
        choice = input('Enter your choice: ')
        if choice == '1':
            authenticate()
            jwt, username = get_jwt_and_username()
            print(f'Retrieved JWT: {jwt[:5]} ..')
            print(f'Hello, {username}')
        elif choice == '2':
            playlists = spotify.list_playlists(jwt)
            for p in playlists['items']:
                print(
                    f'id: {p["id"]},'
                    f' name: {p["name"]},'
                    f' tracks: {p["tracks"]["total"]}')
        elif choice == '3':
            playlist_id_to_reverse = input('Enter playlist id to reverse: ')
            if not len(playlist_id_to_reverse) == 22:
                continue
            playlist_name_to_reverse = 'reversed ' + spotify.get_playlist_name(
                jwt, playlist_id_to_reverse)
            tracks = spotify.list_tracks(jwt, playlist_id_to_reverse)
            print(f'Retrieved {len(tracks["items"])} tracks')
            reversed_playlist_id = spotify.create_playlist(
                jwt, username, playlist_name_to_reverse)['id']
            print(f'New playlist id: {reversed_playlist_id}')
            reversed_ids = []
            for t in tracks['items']:
                reversed_ids.insert(0, t['track']['id'])
            spotify.add_tracks_to_playlist(
                jwt, reversed_playlist_id, reversed_ids)
        elif choice == '4':
            print('Exiting...')
            break
        else:
            print('Invalid choice. Please try again.')


if __name__ == '__main__':
    main()
