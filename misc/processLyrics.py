def process_lyrics(response):
    lyrics = list()
    RawSyncedLyrics = ""
    for line in response.json()["syncedLyrics"].splitlines():
        RawSyncedLyrics = RawSyncedLyrics + line.replace(" ", "", 1) + "\n"
    for line in response.json()["syncedLyrics"].splitlines():
        x = line.split()[0]
        x = x.replace('[', '')
        x = x.replace(']', '')
        seconds = round(float(x.split(':')[1])) + (int(x.split(':')[0]) * 60)
        miliseconds = seconds * 1000
        lyrics.append((line.split(' ', 1)[1], miliseconds))
    return (lyrics, RawSyncedLyrics)