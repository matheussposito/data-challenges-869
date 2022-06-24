import requests

def fetch_lyrics(artist, song):
    url = f'https://lyrics.lewagon.ai/search?artist={artist}&title={song}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['lyrics']
    return 'No lyrics found'