import spotipy, lyricsgenius, time, random, sys, os, pyttsx3, csv, keyboard
from tabulate import tabulate
from spotipy.oauth2 import SpotifyOAuth 
from pyfiglet import Figlet
from termcolor import colored

class VSpotify:
    def __init__(self, sp, genius):
        self.sp = sp
        self.genius = genius
        self.songs_played = []
        self.engine = pyttsx3.init()
        self.figlet = Figlet()

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
    
    def say_song(self, phrase):
        self.engine.say(phrase)
        self.engine.runAndWait()

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
        results = self.sp.search(q=f"track: {song_name} artist:{artist_name}", type="track", limit=50)
        tracks = results['tracks']['items']
        if tracks:
            for track in tracks:
                if track['name'].lower() == song_name.lower():
                    return track
        return None

    def play_song(self, song_uri):
        self.sp.start_playback(uris=[song_uri])

    def get_lyrics(self, artist, song_name):
        song = self.genius.search_song(song_name, artist)
        if song:
            lyrics = song.lyrics.split("\n")
            clean_lyrics = [
                line for line in lyrics if not any(keyword in line.lower() for keyword in ["intro", "outro", "verse 3", "verse 2", "verse 1", "chorus", "pre-chorus", "bridge", "embed", "contributors", "translations"])
            ]
            return "\n".join(clean_lyrics)
        return "Lyrics not found"
    
            
    def display_lyrics_with_timing(self, lyrics, song_uri):
        os.system('cls')
        lines = lyrics.split("\n")

        print("\n🎶 Lyrics 🎶\n")
        
        for i, line in enumerate(lines):
            if keyboard.is_pressed('q'):
                print("returning to dashboard...")
                return

            if self.get_playback_state(song_uri) == "paused":
                print("⏸️ Song is paused... Waiting to resume")
                while self.get_playback_state(song_uri) == "paused":
                    time.sleep(1)

            elif self.get_playback_state(song_uri) == "stopped":
                print("🛑 Song has stopped.")
                return

            print(f"   {line}")  
            time.sleep(0.2)  
        print("\n🎵 Lyrics finished! 🎵")   
        return      
    
    def get_playback_state(self, song_uri):
        playback = self.sp.current_playback()

        if playback:
            if playback.get("is_playing"):
                return "playing" if playback["item"]["uri"] == song_uri else "stopped"
            else:
                return "paused"

    def save(self):
        with open("songs_record.csv", 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["song_name", "frequency"])
            for song in self.songs_played:
                writer.writerow({"song_name" : song['song_name'], "frequency" : song['frequency']})

    def update_songs_played(self, song_name):
        
        # First append the song then update its frequency also
        for i, song_played in enumerate(self.songs_played):
            if song_played['song_name'] == song_name:
                song_played['frequency'] += 1
                return
            
        self.songs_played.append({'song_name' : song_name, 'frequency' : 1})


    def dashboard(self):
            color = colored(self.figlet.renderText("VSpotify"), 'green')
            print(color)
            print("+-----------------------------------------------+")
            print("|                This is VSpotify               |")
            print("+-----------------------------------------------+")
            print("|    (1) Search a song                          |")
            print("|    (2) Choose an artist to listen             |")
            print("|    (3) Print VReceiptify                      |")
            print("|    (4) Exit                                   |")
            print("+-----------------------------------------------+")
            return int(input("Select(1-3): "))
    
    def music_player(self, choice): 
        match choice:
            case 1:
                os.system('cls')
                current_artist, current_song = self.get_current_song()
                print(f"You're currently listening to {current_artist} - {current_song}")
                artist = input("Enter the name of the artist: ")
                song_name = input("Song you want to listen: ") 

                print(f"You're listening to: {artist} - {song_name}")
                print(f"Fetching song from {artist}")
                song = self.get_artist_song(artist, song_name)  

                if song:
                    self.say_song(f"Now playing: {song['name']} by {artist}")
                    self.update_songs_played(song['name'])

                    #Plays song
                    self.play_song(song['uri'])
                    time.sleep(5)

                    #Fetch and display lyrics
                    os.system('cls')
                    lyrics = self.get_lyrics(artist, song['name'])
                    self.display_lyrics_with_timing(lyrics, song['uri'])
                    return
                else:
                    print("Sorry, the requested song was not found.")
                    return

            case 2:
                os.system('cls')
                current_artist, current_song = self.get_current_song()
                print(f"You're currently listening to {current_artist} - {current_song}")
                artist = input("Enter new name of the artist: ")

                print(f"Fetching song from {artist}")
                song = self.get_artist_random_song(artist)  

                if song:
                    print(f"You're listening to: {artist} - {song['name']}")
                    print(f"Now playing: {song['name']}")
                    self.update_songs_played(song['name'])

                    #Plays song
                    self.play_song(song['uri'])
                    time.sleep(5)

                    #Fetch and display lyrics
                    lyrics = self.get_lyrics(artist, song['name'])
                    self.display_lyrics_with_timing(lyrics, song['uri'])

                else:
                    print("Sorry, the requested song was not found.")

                return

            case 3:
                os.system('cls')
                if not self.songs_played:
                    print("No songs yet.")
                    os.system('pause')
                    return
                table_data = [(song['song_name'], song['frequency']) for song in self.songs_played]
                songs = colored(self.figlet.renderText("Receiptify"), color='green')
                print(songs)
                
                print(tabulate(table_data, headers=["Song", "Frequency"], tablefmt="grid"))
                return
            
            case 4:
                os.system('cls')
                self.figlet = Figlet(font='small')
                # saved pdf receiptify
                print(colored(self.figlet.renderText("THIS IS VSpotify"), color='red'))
                print(colored("Irwen Fronda - Programmer", color='light_red'))
                print("\nSaved to VReceiptify.jpg")

                #save to songs_record.csv
                self.save()
                sys.exit(0)
            case _:
                print("Invalid Choice")



def main():
    spotify = VSpotify.get()
    while True: 
        spotify.music_player(spotify.dashboard())



if __name__ == "__main__":
    main()