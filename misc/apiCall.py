import requests
import sys

from misc.processLyrics import process_lyrics
from misc.arguments import args

def api_call(songTitle, songArtist, songAlbum, songDuration):
    songTitle = songTitle.replace(" ", "-")
    songArtist = songArtist.replace(" ", "-")
    songAlbum = songAlbum.replace(" ", "-")

    url = f"https://lrclib.net/api/get?artist_name={songArtist}&track_name={songTitle}&album_name={songAlbum}&duration={songDuration}"
    headers = {
        'User-Agent': f'Unnamed lyric embedding script v0.0.0 no homepage yet'
    }

    if args.debug: print(url)
    elif args.noApiCall: # the point of noApiCall is just to generate the URL for debug purposes
        print(url)
        return -1
    
    try:
        response = requests.get(url, headers)

        if response.status_code == 200:
            if response.json()["syncedLyrics"] == None:
                print(f"{songTitle.replace("-", " ")} has an entry on LRCLIB but no lyrics, is {songTitle} instrumental?")
                return -1
            return process_lyrics(response)
        else:
            print('error ', response.status_code)
            sys.exit()
    except requests.exceptions.RequestException as e:
        print('error ', e)
        sys.exit()