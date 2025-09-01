#!/usr/bin/env python3

#TODO: if no synced lyrics are found in the exact match entry, fail back to non exact searching and give the user a yes/no prompt for the first sync lyrics detected, 
# maybe also allow the user to flip through them with something like confirm/next/failback to unsynced if user doesn't find lyrics they are ok or asks to fail back 
# then do the same with non synced lyrics

#TODO: fix error where what appears to be LRC markdown is tripping up the program, see muscle museum on LRCLib

#TODO: catch errors in the float conversion in process_lyrics() and return -1 if anything happens

#TODO: make flac handler compatible with standard flac synced lyrics

#less important tasks
#TODO: also add the ability to add lyrics with an LRCLIB id

#unimportant tasks
#TODO: add some sort of blank lyric to instrumental songs

import requests
import mutagen
import sys
import json
import os

from misc.arguments import args
from misc.help import print_help

from handlers.mp3 import handle_MP3
from handlers.flac import handle_flac

target = sys.argv[-1]

versionNumber = "vbeta0.0.0"

def main():
    if args.help: print_help()
    if args.target == "": sys.exit()
    if args.recursive:
        if os.path.isdir(target):
            handle_recursion(target)
        else:
            print(f"either {target} doesn't exist or it isn't a directory")
    else:
        if os.path.isfile(target):
            check_compatibility(target)
        else:
            print(f"either {target} doesn't exist or it isn't a file")

def handle_recursion(target):
    if os.path.isdir(target):
        for x in os.listdir(target):
            handle_recursion(os.path.join(target, x))
    else:
        check_compatibility(target)

def check_compatibility(filePath):
    # Messages skipping over WMP system files really clutter up the output so im detecting and silently
    # skipping them
    WMPSystemStrings = {'AlbumArtSmall.jpg', 'Folder.jpg'}
    # i hate this but can't think of a nicer way to do it, i'm terrible at python so if there is one please
    # do let me know
    filename = filePath.rsplit("\\", 1)[1]
    if filename in WMPSystemStrings\
    or filename.startswith("AlbumArt_") and filename.endswith("_Large.jpg")\
    or filename.startswith("AlbumArt_") and filename.endswith("_Small.jpg"):
        if args.debug: print("DEBUG: Ignoring system file", filePath)
        return
    
    fileExtension = filePath.rsplit(".", 1)[1]
    print(filePath)
    match fileExtension:
        case "mp3":
            handle_MP3(filePath)
        case "flac":
            handle_flac(filePath)
        case _:
            print(f"{filePath} this script currently only supports mp3 and flac files, sorry TwT")
    
main()