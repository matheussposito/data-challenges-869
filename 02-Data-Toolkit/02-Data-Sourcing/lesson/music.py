import requests

def fetch_lyrics(artist, title):
    url = f'https://lyrics.lewagon.ai/search?artist={artist}&title={title}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['lyrics']
    return 'No lyrics'
