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
                print(f"{songTitle.replace("-", " ")} has an entry on LRCLIB but no syncronised lyrics,")
                if response.json()["plainLyrics"] != None:
                    print("Unsynchronised lyrics were found, do you want to failback to unsynchronised lyrics, keep looking for syncronised lyrics or skip this song?\n\
                          [F]ailback, [K]eep looking, [S]kip")
                else: print ("This song has a LRCLIB entry but lyrics were not found, do you want to keep looking or skip this song?\n\
                             [K]eep looking, [S]kip")
                while True:
                    match input():
                        case "F" | "f":
                            if response.json()["plainLyrics"] == None: continue
                            return process_lyrics(response, False)
                        case "K" | "k":
                            print("keep looking isn't implemented yet, sorry TwT")
                            return -1
                        case "S" | "s":
                            print("skipping this song")
                            return -1
                        case _: continue
            return process_lyrics(response)
        else:
            print('error ', response.status_code)
            sys.exit()
    except requests.exceptions.RequestException as e:
        print('error ', e)
        sys.exit()