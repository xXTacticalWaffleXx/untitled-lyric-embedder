changes in **bold** are ones that i need to do before i consider this
"functional"

# bug fixes

fix error where what appears to be LRC markdown is tripping up the program, 
see muscle museum on LRCLib

fix issue where album metadata with an & sign breaks the api call, see
peace & love by dylan brady
# Important changes

**catch errors in the float conversion in process_lyrics() and print an error 
message requesting the bug be reported to me / return -1 if anything happens**

**add separate modes for musicolet compatibility and compatibility with players
that are expecting plain unsynced lyrics**

add an option to import lyrics from a text file

**implement the argparse library instead of handrolling my own function**
# less important
also add the ability to add lyrics with an LRCLIB id

# unimportant tasks
add some sort of blank lyric to instrumental songs