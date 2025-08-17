#!/usr/bin/env python3

#TODO: failback to just providing a seperate lyrics file if an embed handler doesn't exist
#TODO: make script exit on api call failure, current behaviour will try to set the lyrics to "1"

import requests
import mutagen
import sys
import json
import os

import arguments

from mutagen.id3 import ID3, SYLT, Encoding, USLT
from mutagen.mp3 import MP3

target = sys.argv[-1]
args = arguments.handler()

def main():
    if args.recursive:
        if os.path.isdir(target):
            for x in os.listdir(target):
                check_compatibility(target + "/" + x)
        else:
            print(f"either {target} doesn't exist or it isn't a directory")
    else:
        if os.path.isfile(target):
            check_compatibility()
        else:
            print(f"either {target} doesn't exist or it isn't a file")
        

def check_compatibility(fileName):
    fileExtension = fileName.rsplit(".", 1)[1]
    if fileExtension == "mp3":
        Handle_MP3(fileName)
    else:
        print("this script currently only supports mp3 files, sorry TwT")

def api_call(songTitle, songArtist, songAlbum, songDuration):
    songTitle = songTitle.replace(" ", "-")
    songArtist = songArtist.replace(" ", "-")
    songAlbum = songAlbum.replace(" ", "-")

    url = f"https://lrclib.net/api/get?artist_name={songArtist}&track_name={songTitle}&album_name={songAlbum}&duration={songDuration}"

    headers = {
        'User-Agent': 'Unnamed lyric embedding script vbeta0.0.1 no homepage yet'
    }
    print(url)
    
    try:
        response = requests.get(url, headers)

        if response.status_code == 200:
            lyrics = list()
            RawSyncedLyrics = ""
            for line in response.json()["syncedLyrics"].splitlines():
                RawSyncedLyrics = RawSyncedLyrics + line.replace(" ", "", 1) + "\n"
            for line in response.json()["syncedLyrics"].splitlines():
                x = line.split()[0]
                x = x.replace('[', '')
                x = x.replace(']', '')
                seconds = round(float(x.split(':')[1])) + (int(x.split(':')[0]) * 60)
                miliseconds = seconds * 1000

                lyrics.append((line.split(' ', 1)[1], miliseconds))
            return (lyrics, RawSyncedLyrics)
        else:
            print('error ', response.status_code)
            return 1
    except requests.exceptions.RequestException as e:
        print('error ', e)
        return 1
    
def Handle_MP3(fileName):
    print("dingus")
    audioTags = ID3(fileName)

    songTitle = str(audioTags.get('TIT2'))
    songArtist = str(audioTags.get('TPE1'))
    songAlbum = str(audioTags.get('TALB'))

    audio = MP3(fileName) # ID3 is only the tags and duration isn't stored in ID3 tags, we have to use streaminfo
    songDuration = round(float(audio.info.pprint().split(", ")[4].split()[0])) # i get the distinct impression this is a fucking terrible way to do this, if anyone has a better idea please do let me know
    
    lyrics = api_call(songTitle, songArtist, songAlbum, songDuration)
    RawSyncedLyrics = lyrics[1]

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
    print(RawSyncedLyrics)
    audioTags.setall('USLT', [USLT(
        encoding=Encoding.UTF8,
        lang="   ",
        format=2,
        type=1,
        text=RawSyncedLyrics
    )])
    audioTags.save(v2_version=3)
    return 0

main()