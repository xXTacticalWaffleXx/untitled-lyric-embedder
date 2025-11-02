#!/usr/bin/env python3

import requests
import mutagen
import sys
import json
import os
import signal

from .misc.arguments import args
from .misc.help import print_help

from .handlers.mp3 import handle_MP3
from .handlers.flac import handle_flac

target = sys.argv[-1]

versionNumber = "vbeta0.0.0"

def SIGINThandler(signum, frame):
    print()
    print("Ctrl+C received, exiting")
    sys.exit()


def main():
    signal.signal(signal.SIGINT, SIGINThandler)
    if args.help: print_help()
    if args.target == "": sys.exit()
    if args.debug: print("DEBUG: " + target)
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
    filename = filePath
    if "\\" in filename: filename = filePath.rsplit("\\", 1)[1] #only get the name of the file, not the full path
    if "/" in filename: filename = filePath.rsplit("/", 1)[1] #only get the name of the file, not the full path
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