import requests
import sys

from untitled_lyric_embedder.misc.processLyrics import process_lyrics
from untitled_lyric_embedder.misc.arguments import args

from untitled_lyric_embedder.api.fuzzySearch import fuzzySearch
from untitled_lyric_embedder.api.headers import headers

noLyricMessage = '''no lyrics were found in this songs entry, is this song instrumental? Do you want to keep looking or skip this song?\n\
[K]eep looking, [S]kip '''

noSyncedLyricsMessage = '''Unsynchronised lyrics were found, do you want to failback to unsynchronised lyrics, keep looking for syncronised lyrics or skip this song?\n\
[F]ailback, [K]eep looking, [S]kip '''

instrumentalMessage = 'This song is taged as instrumental on LRCLib: skipping'

def api_call(song):
    humanReadableSongTitle = song.title
    song.title = song.title.replace(" ", "-")
    song.artist = song.artist.replace(" ", "-")
    song.album = song.album.replace(" ", "-")

    url = f"https://lrclib.net/api/get?artist_name={song.artist}&track_name={song.title}&album_name={song.album}&duration={song.duration}"


    if args.debug: print(url)
    elif args.noApiCall: # the point of noApiCall is just to generate the URL for debug purposes
        print(url)
        return -1
    
    if args.forceFuzzy:
        v = fuzzySearch(song, None)
        return process_lyrics(v[0], v[1], v[2])

    try:
        response = requests.get(url, headers)

        if response.status_code == 200:
            if response.json()["syncedLyrics"] == None:
                print(f"{humanReadableSongTitle}:")
                if response.json()["instrumental"]: 
                    print(instrumentalMessage)
                    return -1
                elif response.json()["plainLyrics"] != None:
                    print(noSyncedLyricsMessage, end="")
                else: print (noLyricMessage, end="")
                while True:
                    user_input = str()
                    if args.autoContinueSearch: user_input = "k"
                    if args.autoFailback: user_input = "f"
                    if args.autoSkip: user_input = "s"
                    if user_input == "": user_input = input()
                    match user_input:
                        case "F" | "f" | args.autoFailback:
                            if response.json()["plainLyrics"] == None: continue
                            return process_lyrics(response)
                        case "K" | "k" | args.autoContinueSearch:
                            v = fuzzySearch(song, response)
                            return process_lyrics(v[0], v[1], v[2])
                        case "S" | "s" | args.autoSkip:
                            print("skipping this song")
                            return -1
                        case _: continue

            return process_lyrics(response)
        else:
            if response.status_code == 404:
                print(f"error 404: An entry for {humanReadableSongTitle} could not be found on LRCLIB, is the metadata of this file correct?")
            else:
                print('error', response.status_code)
            return -1
    except requests.exceptions.RequestException as e:
        print('error ', e, 'please report this to me on github')
        sys.exit()