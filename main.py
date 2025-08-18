#!/usr/bin/env python3

#TODO: failback to just providing a seperate lyrics file if an embed handler doesn't exist
#TODO: move format handler functions to a seperate file
#TODO: for some reason when ran on my bullets folder the script is failing on an invisible file called "AlbumArtSmall.jpg"
#TODO: recursion isn't true recursion, I.E if script is ran on a folder containing subfolders even with the recursive flag not only wont those subfolders not be scanned they will cause an exception
#TODO: a 404 shouldn't cause the script to exit in recursive mode
#TODO: make script failback to plain lyrics if synced fails
#TODO: how the fuck do i handle multiple lyrics entries like with butterfly knife, maybe send the tags to the /ap/search endpoint
#TODO: also add the ability to add lyrics with an LRCLIB id

#TODO: if no synced lyrics are found in the exact match entry, fail back to non exact searching and give the user a yes/no prompt for the first sync lyrics detected, maybe also allow the user to flip through them with something like confirm/next/failback to unsynced
# if user doesn't find lyrics they are ok or asks to fail back then do the same with non synced lyrics

#unimportant tasks
#TODO: add some sort of blank lyric to instrumental songs

import requests
import mutagen
import sys
import json
import os

import arguments
from help import print_help

from mutagen.id3 import ID3, SYLT, Encoding, USLT
from mutagen.mp3 import MP3

target = sys.argv[-1]
args = arguments.handler()

versionNumber = "vbeta0.0.0"

def main():
    if args.target == "": sys.exit()
    if args.help:
        print_help()
    if args.recursive:
        if os.path.isdir(target):
            for x in os.listdir(target):
                check_compatibility(target + "/" + x)
        else:
            print(f"either {target} doesn't exist or it isn't a directory")
    else:
        if os.path.isfile(target):
            check_compatibility(target)
        else:
            print(f"either {target} doesn't exist or it isn't a file")
        

def check_compatibility(fileName):
    fileExtension = fileName.rsplit(".", 1)[1]
    if fileExtension == "mp3":
        print(fileName)
        Handle_MP3(fileName)
    else:
        print(f"{fileName} this script currently only supports mp3 files, sorry TwT")

def api_call(songTitle, songArtist, songAlbum, songDuration):
    songTitle = songTitle.replace(" ", "-")
    songArtist = songArtist.replace(" ", "-")
    songAlbum = songAlbum.replace(" ", "-")

    url = f"https://lrclib.net/api/get?artist_name={songArtist}&track_name={songTitle}&album_name={songAlbum}&duration={songDuration}"

    headers = {
        'User-Agent': f'Unnamed lyric embedding script v0.0.0 no homepage yet'
    }
    if args.debug: print(url)
    
    try:
        response = requests.get(url, headers)

        if response.status_code == 200:
            lyrics = list()
            RawSyncedLyrics = ""
            if response.json()["syncedLyrics"] == None:
                print(f"{songTitle.replace("-", " ")} has an entry on LRCLIB but no lyrics, is {songTitle} instrumental?")
                return -1
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
            sys.exit()
    except requests.exceptions.RequestException as e:
        print('error ', e)
        sys.exit()
    
def Handle_MP3(fileName):
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

main()