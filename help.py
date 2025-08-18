help = f"""
Luna's untitled lyric embedder

-h: Show this message
-d: Show debug information
-D: Dry run, prints lyrics instead of embedding them into files
-r: Recursive mode, runs this script for every compatible file in a specified folder
-N: Prints the API URL without making a call to the API or 
"""

def print_help():
    print(help)