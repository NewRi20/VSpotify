import spotipy
from spotipy.oauth2 import SpotifyOAuth 
import lyricsgenius
import time
import random
import pygame

# Spotify API credentials
SPOTIFY_CLIENT_ID = "dcad3cc011e24eb48625bc87386dcb78"
SPOTIFY_CLIENT_SECRET = "fcd95721bc614a059d2322acf9d9a915"
SPOTIFY_REDIRECT_URI = "https://google.com"

# Genius API credentials
GENIUS_ACCESS_TOKEN = "k4Ycmv-LGKvi1eoR4mE9KqBqSLIwWSajof3qR-eWibSrkQQvpWAu6cw6KiGf_wUS"

# Authentication with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-read-playback-state,user-modify-playback-state,user-read-currently-playing"
))
  
# Genius API client
genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN)
   
# Function to get currently playing song
def get_current_song():
    current_track = sp.current_playback()
    if current_track:
        artist = current_track['item']['artists'][0]['name']
        song_name = current_track['item']['name']
        return artist, song_name
    return None, None

# Function to search for an artist and get 5 random songs
def get_artist_songs(artist_name):
    results = sp.search(q=f"artist:{artist_name}", type="track", limit=50)
    tracks = results['tracks']['items']
    selected_songs = random.sample(tracks, 5) if len(tracks) >= 5 else tracks
    return selected_songs

# Function to play song
def play_song(song_uri):
    sp.start_playback(uris=[song_uri])

# Function to get lyrics from Genius
def get_lyrics(artist, song_name):
    try:
        song = genius.search_song(song_name, artist)
        return song.lyrics if song else "Lyrics not found."
    except:
        return "Lyrics not found."

# Function to display lyrics with timing
def display_lyrics_with_timing(lyrics):
    lines = lyrics.split("\n")
    for line in lines:
        print(line)
        time.sleep(2)  # Adjust timing as needed

# Main execution
if __name__ == "__main__":
    print("Fetching current song...")
    artist, song_name = get_current_song()

    if artist:
        print(f"You're listening to: {artist} - {song_name}")

        print(f"Fetching songs from {artist}...")
        songs = get_artist_songs(artist)

        played_songs = []

        for song in songs:
            print(f"Now playing: {song['name']}")
            played_songs.append(song['name'])

            # Play song on Spotify
            play_song(song['uri'])
            time.sleep(5)  # Let the song start

            # Fetch and display lyrics
            lyrics = get_lyrics(artist, song['name'])
            display_lyrics_with_timing(lyrics)

            # Wait before playing the next song
            time.sleep(10)

        print("\nSongs Played:")
        for song in played_songs:
            print(f"- {song}")
    else:
        print("No song is currently playing.")
