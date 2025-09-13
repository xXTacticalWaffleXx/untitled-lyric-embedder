from mutagen.id3 import ID3, SYLT, Encoding, USLT
from mutagen.mp3 import MP3

from api.apiCall import api_call
from misc.arguments import args

def handle_MP3(fileName):
    audioTags = ID3(fileName)
    songTitle = str(audioTags.get('TIT2'))
    songArtist = str(audioTags.get('TPE1'))
    songAlbum = str(audioTags.get('TALB'))
    audio = MP3(fileName) # ID3 is only the tags and duration isn't stored in ID3 tags, we have to use streaminfo
    songDuration = round(float(audio.info.pprint().split(", ")[4].split()[0])) # i get the distinct impression this is a fucking terrible way to do this, if anyone has a better idea please do let me know
    api_results = api_call(songTitle, songArtist, songAlbum, songDuration)
    if api_results != -1:
        lyrics = api_results
    else:
        return
    RawSyncedLyrics = lyrics[1]
    if args.dryRun:
        print(RawSyncedLyrics)
    else:
        audioTags.setall('SYLT', [SYLT(
            encoding=Encoding.UTF8,
            lang="eng",
            format=2,
            type=1,
            text=lyrics[0]
        )])
        # fuck musicolet, musicolet is my fucking opp, for some fucking bastard
        # reason, musicolet wants syncronised lyrics to be embeded into the
        # non synced lyrics tag
        audioTags.setall('USLT', [USLT(
            encoding=Encoding.UTF8,
            lang="   ",
            format=2,
            type=1,
            text=RawSyncedLyrics
        )])
        audioTags.save(v2_version=3)
        return 0