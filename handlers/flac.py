from mutagen.flac import FLAC, StreamInfo

from misc.apiCall import api_call
from misc.arguments import args

def handle_flac(filename):
    audio = FLAC(filename)
    songTitle = str(audio['title'])
    songArtist = str(audio['artist'])
    songAlbum = str(audio['album'])
    
    songLength = str(round(audio.info.length))
    apiResults = api_call(songTitle, songArtist, songAlbum, songLength)
    if apiResults == -1: return
    rawSyncedLyrics = apiResults[1]
    if args.dryRun: print(rawSyncedLyrics); return
    audio["unsyncedlyrics"] = rawSyncedLyrics
    audio.save()