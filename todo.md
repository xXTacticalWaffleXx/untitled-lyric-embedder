# bug fixes

fix error where what appears to be LRC markdown is tripping up the program, 
see muscle museum on LRCLib

make flac handler compatible with standard flac synced lyrics

# Important changes
If no synced lyrics are found in the exact match entry, fail back to non 
exact searching and give the user a yes/no prompt for the first sync lyrics 
detected, maybe also allow the user to flip through them with something like 
confirm/next/failback to unsynced if user doesn't find lyrics they are ok or 
asks to fail back then do the same with non synced lyrics

catch errors in the float conversion in process_lyrics() and print an error 
message requesting the bug be reported to me / return -1 if anything happens

add separate modes for musicolet compatibility and compatibility with players
that are expecting plain unsynced lyrics

add an option to import lyrics from a text file

add option to force fuzzy search

# less important
also add the ability to add lyrics with an LRCLIB id

# unimportant tasks
add some sort of blank lyric to instrumental songs