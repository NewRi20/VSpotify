import spotipy, lyricsgenius, time, random, sys
from spotipy.oauth2 import SpotifyOAuth 


import pygame

class VSpotify:
    def __init__(self, sp, genius):
        self.sp = sp
        self.genius = genius
        self.played_songs = []

    @classmethod
    def get(cls):
        # Spotify API credentials
        SPOTIFY_CLIENT_ID = "dcad3cc011e24eb48625bc87386dcb78"
        SPOTIFY_CLIENT_SECRET = "fcd95721bc614a059d2322acf9d9a915"
        SPOTIFY_REDIRECT_URI = "https://google.com"
        

        # Genius API credentials
        GENIUS_ACCESS_TOKEN = "k4Ycmv-LGKvi1eoR4mE9KqBqSLIwWSajof3qR-eWibSrkQQvpWAu6cw6KiGf_wUS"
        
        # Genius API client
        genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN)

        # Authentication with Spotify
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope="user-read-playback-state,user-modify-playback-state,user-read-currently-playing"
        ))
        return cls(sp, genius)
    
    def get_current_song(self):
        current_track = self.sp.current_playback()
        if current_track:
            artist = current_track['item']['artists'][0]['name']
            song = current_track['item']['name']
            return artist, song
        return None, None

    def get_artist_random_song(self, artist_name):
        results = self.sp.search(q=f"artist:{artist_name}", type="track", limit=50)
        tracks = results['tracks']['items']
        if tracks:
            return random.choice(tracks)
        return None

    def get_artist_song(self, artist_name, song_name):
        results = self.sp.search(q=f"artist:{artist_name}", type="track", limit=50)
        tracks = results['tracks']['items']
        if tracks:
            for track in tracks:
                if track['name'].lower() == song_name.lower():
                    return track
        return None

    def play_song(self, song_uri):
        self.sp.start_playback(uris=[song_uri])

    def get_lyrics(self, artist, song_name):
        try:
            song = self.genius.search_song(song_name, artist)
            return song.lyrics if song else "Lyrics not found."
        except:
            return "Lyrics not found"
    
    def display_lyrics_with_timing(self,lyrics):
        lines = lyrics.split("\n")
        for line in lines:
            print(line)
            time.sleep(2)
    
    def dashboard(self):
            print("+-----------------------------------------------+")
            print("|                This is VSpotify               |")
            print("+-----------------------------------------------+")
            print("|    (1) Search a song                          |")
            print("|    (2) Search a song from liked songs library |")
            print("|    (3) Choose an artist to listen             |")
            print("|    (4) Exit and Print VReceiptify             |")
            print("+-----------------------------------------------+")
            return int(input("Select(1-4): "))
    
    def music_player(self, choice): 
        match choice:
            case 1:
                ...
            case 2:
                ...
            case 3:
                print("No song is currently playing.")
                artist = input("Enter the name of the artist: ")
                song_name = input("Song you want to listen: ")

                print(f"You're listening to: {artist} - {song_name}")
                print(f"Fetching song from {artist}")
                song = self.get_artist_song(artist, song_name)  

                if song:
                    print(f"Now playing: {song['name']}")
                    self.played_songs.append(song['name'])

                    #Plays song
                    self.play_song(song['uri'])
                    time.sleep(5)

                    #Fetch and display lyrics
                    lyrics = self.get_lyrics(artist, song['name'])
                    self.display_lyrics_with_timing(lyrics)

                else:
                    print("Sorry, the requested song was not found.")

                return

            case 4:
                print("\nSongs Played:")
                for song in self.played_songs:
                    print(f"- {song}")
                sys.exit(0)
                
            case _:
                print("Invalid Choice")



def main():
    spotify = VSpotify.get()
    while True: 
        spotify.music_player(spotify.dashboard())



if __name__ == "__main__":
    main()