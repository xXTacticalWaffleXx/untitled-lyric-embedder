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