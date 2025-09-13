from mutagen.flac import FLAC, StreamInfo

from api.apiCall import api_call
from misc.arguments import args
from misc.songMetadata import songMetadata

def handle_flac(filename):
    audio = FLAC(filename)
    song = songMetadata(audio['title'], audio['artist'], audio['album'], str(round(audio.info.length)))
    
    apiResults = api_call(song)
    if apiResults == -1: return
    rawSyncedLyrics = apiResults[1]
    if args.dryRun: print(rawSyncedLyrics); return
    audio["unsyncedlyrics"] = rawSyncedLyrics
    audio.save()