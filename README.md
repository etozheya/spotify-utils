# Spotify-Utils

Python package that provides utilities for interacting with the Spotify API.
Currently, it includes functionality to create a reversed playlist on Spotify.


## Features

* Reverse Playlist Creation: Create a new playlist on Spotify with the tracks
reversed from an existing playlist.


## Requirements

* Python
* Requests library


## Usage

### Setup

* [Create Spotify app](https://developer.spotify.com/documentation/web-api)
  * [Log into the dashboard](https://developer.spotify.com/dashboard)
  * Create a `Web API` app
  * Grab `client id`, `client secret` and `redirect url` from the app
* Clone this repo
```commandline
git clone https://github.com/etozheya/spotify-utils.git
```
* Insert credentials from your app into the `credentials.json` file
* Install required packages
```commandline
pip install -r requirements.txt
```
* Run the main script
```commandline
python main.py
```
* **Important:** every time you run the script or relogin you will be redirected 
to a browser, copy the code from the url after the `code=`. It is required for authentication.

### Wrapped

1. Request your data [here](https://www.spotify.com/uk/account/privacy/)
2. Save the json files into the `wrapped` folder
3. Adjust configuration variables at the top of the `main.py` file

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, 
or feature requests, please open an issue on GitHub.
