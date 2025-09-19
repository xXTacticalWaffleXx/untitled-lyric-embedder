import requests

from api.headers import headers
from misc.arguments import args

mode = "syncedLyrics"

def api_call_fuzzy(url):
    response = requests.get(url, headers)

    if response.status_code == 200:
        print(len(response.json()))
        for _ in range(len(response.json())):
            if response.json()[_] == None: break
            if response.json()[_][mode] == None: continue
            print(response.json()[_][mode])
            print("Are these the lyrics you're looking for? [y/n]")
            while True:
                user_input = str(input())
                match user_input:
                    case "y" | "Y":
                        if mode == "syncedLyrics" : return (response, _, False)
                        else: return (response, _, False)
                    case "N" | "n":
                        break
        return -1

def fuzzySearch(song, plainLyrics):
    global mode
    if args.debug: print("[DEBUG] fuzzy search mode 1")
    url = f"https://lrclib.net/api/search?artist_name={song.artist}&track_name={song.title}&album_name={song.album}"
    if args.debug: print("[DEBUG] ", url)
    v = api_call_fuzzy(url)
    if v != -1: return v
    if args.debug: print("[DEBUG] fuzzy search mode 2")
    url = f"https://lrclib.net/api/search?track_name={song.title}&album_name={song.album}"
    if args.debug: print("[DEBUG] ", url)
    v = api_call_fuzzy(url)
    if v != -1: return v
    if args.debug: print("[DEBUG] fuzzy search mode 3")
    url = f"https://lrclib.net/api/search?artist_name={song.artist}&track_name={song.title}"
    if args.debug: print("[DEBUG] ", url)
    v = api_call_fuzzy(url)
    if v != -1: return v
    if args.debug: print("[DEBUG] fuzzy search mode 4")
    url = f"https://lrclib.net/api/search?track_name={song.title}"
    if args.debug: print("[DEBUG] ", url)
    v = api_call_fuzzy(url)
    if v != -1: return v
    
    if mode == "syncedLyrics":
        print("Syncronised lyrics were unable to be found")
        if plainLyrics != None: 
            print("Unsyncronised lyrics were found in the exact search, would you like to failback to them")
            print("[Y]es/[P]review/Non exact [S]earch for unsynced lyrics/[N]o")
            while True:
                user_input = input()
                match user_input:
                    case "Y" | "y":
                        return(plainLyrics, -1, True)
                    case "P" | "p":
                        print(plainLyrics["plainLyrics"])
                        print("[Y]es/[P]review/Non exact [S]earch for unsynced lyrics/[N]o")
                    case "S" | "s":
                        mode = "plainLyrics"
                        return fuzzySearch(song, plainLyrics)
                    case "N" | "n":
                        return -1

        else:
            print("Would you like to search for unsyncronised lyrics")
            print("Y/n")
            while True:
                user_input = input()
                match user_input:
                    case "Y" | "y":
                        mode = "plainLyrics"
                        fuzzySearch()
                    case "N" | "n":
                        return -1
    else:
        print("Sorry no lyrics could be found")
        return -1