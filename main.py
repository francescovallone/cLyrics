import spotipy
from spotipy.oauth2 import SpotifyOAuth
from lyricsgenius import Genius
import credentials
from math import ceil
from time import sleep


class PrintCodes:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=credentials.CLIENT_ID,
                                               client_secret=credentials.CLIENT_SECRET,
                                               redirect_uri=credentials.REDIRECT_URI,
                                               scope="user-read-playback-state"))

genius = Genius(credentials.GENIUS_ACCESS_TOKEN)


def get_lyrics(song, artists, album, image, duration):
    print("{0}{1} ({3}){2}".format(PrintCodes.BOLD, song, PrintCodes.END, album))
    print(PrintCodes.PURPLE,end='')
    for x in range(0, len(artists)):
        if x != len(artists)-1: print(artists[x], end=' - ')
        else: print(artists[x])
    print(PrintCodes.END)
    song_genius = genius.search_song(song, artists[0], get_full_info=False)
    lyrics = song_genius.lyrics.split('\n')
    for line in lyrics:
        if '[' in line: print("{0}{1}{2}{3}".format(PrintCodes.UNDERLINE, PrintCodes.YELLOW, line, PrintCodes.END))
        else: print(line)


def main():
    results = sp.current_playback()
    artists = [artist['name'] for artist in results['item']['artists']]
    song = results['item']['name']
    album = results['item']['album']['name']
    image = results['item']['album']['images'][1]
    playing = results['is_playing']
    duration = int(ceil(results['item']['duration_ms']/1000))
    if playing is True:
        get_lyrics(song, artists, album, image, duration)


if __name__ == "__main__":
    main()
