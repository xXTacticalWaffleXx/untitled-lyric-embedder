def process_lyrics(response, result = -1, usePlain = False):
    if result != -1: 
        response_json = response.json()[result]
    else: 
        response_json = response.json()

    if usePlain == False:    
        if response_json["syncedLyrics"] != None: isSynced = True
        else: isSynced = False
    else: isSynced = False
    
    if isSynced:
        SYLTLyrics = list()
        USLTLyrics = ""
        for line in response_json["syncedLyrics"].splitlines():
            if "] " not in line: line = line.replace(']', '] ')
            USLTLyrics = USLTLyrics + line.replace(" ", "", 1) + "\n"
        # This code is supposed to handle standards compliant ID3 syncronised lyrics
        # However every player i have seen so far has respected LRC formated lyrics
        # embeded into the unsyncronised lyrics tag, I'm going to get this working
        # eventually but at the moment its not a priority, if this script doesn't
        # work for your player, specifically your player can handle syncronised
        # embeded lyrics and you are seeing LRC formatted time stamps in
        # unsyncronised lyrics, please get in touch with me over github with
        # the song you're trying to listen to and the player you're trying to use
        #
        # for line in response.json()["syncedLyrics"].splitlines():
        #     if "] " not in line: line = line.replace(']', '] ')
        #     x = line.split()[0]
        #     x = x.replace('[', '')
        #     x = x.replace(']', '')
        #     seconds = round(float(x.split(':')[1])) + (int(x.split(':')[0]) * 60)
        #     miliseconds = seconds * 1000
        #     SYLTLyrics.append((line.split(' ', 1)[1], miliseconds))
    else:
        SYLTLyrics = ""
        USLTLyrics = response_json["plainLyrics"]
    return (SYLTLyrics, USLTLyrics, isSynced)