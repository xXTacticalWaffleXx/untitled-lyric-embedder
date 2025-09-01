def process_lyrics(response, isSynced = True):
    if isSynced:
        SYLTLyrics = list()
        USLTLyrics = ""
        for line in response.json()["syncedLyrics"].splitlines():
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
        USLTLyrics = response.json()["plainLyrics"]
    return (SYLTLyrics, USLTLyrics, isSynced)