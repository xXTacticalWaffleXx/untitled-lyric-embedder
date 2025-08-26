#!/usr/bin/env python3

#TODO: for some reason when ran on my bullets folder the script is failing on an invisible file called "AlbumArtSmall.jpg"
#TODO: recursion isn't true recursion, I.E if script is ran on a folder containing subfolders even with the recursive flag not only wont those subfolders not be scanned they will cause an exception
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

from misc.arguments import args
from misc.help import print_help
from handlers.mp3 import handle_MP3

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

def check_compatibility(fileName):
    fileExtension = fileName.rsplit(".", 1)[1]
    if fileExtension == "mp3":
        print(fileName)
        handle_MP3(fileName)
    else:
        print(f"{fileName} this script currently only supports mp3 files, sorry TwT")
    
main()