help = f"""
Luna's untitled lyric embedder

-h: Show this message
-d: Show debug information
-D: Dry run, prints lyrics instead of embedding them into files
-r: Recursive mode, runs this script for every compatible file in a specified folder
-N: Prints the API URL without making a call to the API or 
--lyrics-autoSkip: automatically skip songs without syncronised lyrics
--lyrics-autoContiune: automatically continue searching for syncronised lyrics if none are found at first
--lyrics-autoFailback: automatically failback to unsyncronised lyrics if synchronised lyrics cann't be found but syncronised lyrics can
--force-fuzzy-search: force non exact searching
"""

def print_help():
    print(help)