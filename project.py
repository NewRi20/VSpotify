import spotipy, lyricsgenius, time, random, sys, os, pyttsx3, csv, keyboard
from tabulate import tabulate
from spotipy.oauth2 import SpotifyOAuth 
from pyfiglet import Figlet
from termcolor import colored

class VSpotify:

    def __init__(self, sp, genius):
        try:
            self.sp = sp
            self.genius = genius
            self._songs_played = []
            self.figlet = Figlet()
        except Exception as e:
            print(e)
            sys.exit(0)

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
    

    def get_song_list(self):
        return self._songs_played


    def get_current_song(self):
        try:
            current_track = self.sp.current_playback()
            if current_track:
                artist = current_track['item']['artists'][0]['name']
                song = current_track['item']['name']
                return artist, song
        except Exception as e:
            print("Error in getting current song: {e}")
    
        return None, None
        

    def get_artist_random_song(self, artist_name):
        artist_name = artist_name.strip().lower()
        results = self.sp.search(q=f"artist:{artist_name}", type="track", limit=10)
        tracks = results['tracks']['items']
        if tracks:
            return random.choice(tracks)
        return None


    def get_artist_song(self, artist_name, song_name):
        artist_name = artist_name.strip().lower()
        song_name = song_name.strip().lower()
        results = self.sp.search(q=f"track:{song_name} artist:{artist_name}", type="track", limit=10)
        tracks = results['tracks']['items']
        if tracks:
            for track in tracks:
                if song_name.lower() in track['name'].lower():
                    return track
        return None
    

    def get_song_duration(self, artist_name, song_name):
        time.sleep(1)
        artist_name = artist_name.strip()
        song_name = song_name.strip()
        result = self.sp.search(q=f"track:{song_name} artist:{artist_name}", type='track', limit=1)
        
        if result['tracks']['items']:
            track_id = result['tracks']['items'][0]['id']

            track = self.sp.track(track_id)
            duration_ms = track['duration_ms']

            duration_sec = duration_ms / 1000
            minutes = int(duration_sec // 60)
            seconds = int(duration_sec % 60)

            return f"{minutes}:{seconds}"
        else:
            print(f"No track-duration found for {artist_name} - {song_name}")
            return None, None


    def play_song(self, song_uri):
        self.sp.start_playback(uris=[song_uri])


    def get_lyrics(self, artist, song_name):
        time.sleep(1)
        try:
            artist = artist.strip()
            song_name = song_name.strip()

            song = self.genius.search_song(song_name, artist)
            if song and song.lyrics:
                lyrics = song.lyrics.split("\n")
                clean_lyrics = [
                    line for line in lyrics if not any(keyword in line.lower() for keyword in ["refrain", "intro", "outro", "verse 3", "verse 2", "verse 1", "chorus", "pre-chorus", "bridge", "embed", "contributors", "translations"])
                ]
                return "\n".join(clean_lyrics)
        except Exception as e:
            print(f"Error fetching lyrics: {e}")
            return "Lyrics not found"
        
        return "Lyrics not found"
    
                
    def display_lyrics_with_timing(self, lyrics, song_uri):
        os.system('cls')
        lines = lyrics.split("\n")

        print("\n🎶 Lyrics 🎶\n")
        
        for i, line in enumerate(lines):
            if keyboard.is_pressed('q'):
                print("\n\nReturning to dashboard...")
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
                         

    def update_songs_played(self, song_name, song_duration):
        
        # First append the song then update its frequency also
        for i, song_played in enumerate(self._songs_played):
            if song_played['song_name'] == song_name:
                song_played['frequency'] += 1
                return
            
        self._songs_played.append({'frequency' : 1, 'song_name' : song_name, 'duration': song_duration})
    


    def dashboard(self):
            color = colored(self.figlet.renderText("VSpotify"), 'green')
            print(color)
            try:
                print("+-----------------------------------------------+")
                print("|                This is VSpotify               |")
                print("+-----------------------------------------------+")
                print("|    (1) Search a song                          |")
                print("|    (2) Choose an artist to listen             |")
                print("|    (3) Print VReceiptify                      |")
                print("|    (4) Exit                                   |")
                print("+-----------------------------------------------+")
                return int(input("Select(1-3): "))
            except ValueError:
                print("Invalid Input...")
    

    def music_player(self, choice): 
        match choice:
            case 1:
                os.system('cls')
                current_artist, current_song = self.get_current_song()
                if not current_artist and not current_song:
                    print("No song currently playing.")
                    current_artist, current_song = "Unknown", "Unknown"

                print(f"You're currently listening to {current_artist} - {current_song}")
                artist = input("Enter the name of the artist: ")
                song_name = input("Song you want to listen: ") 

                print(f"You're listening to: {artist} - {song_name}")
                print(f"Fetching song from {artist}")
                song = self.get_artist_song(artist, song_name)
                song_duration = self.get_song_duration(artist, song_name)  

                if song:
                    say_song(f"Now playing: {song['name']} by {artist}")
                    self.update_songs_played(song['name'], song_duration)

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
                    song_duration = self.get_song_duration(artist, song['name']) 

                    say_song(f"Now playing: {song['name']} by {artist}")
                    self.update_songs_played(song['name'], song_duration)

                    #Plays song
                    self.play_song(song['uri'])
                    time.sleep(5)

                    #Fetch and display lyrics
                    lyrics = self.get_lyrics(artist, song['name'])
                    self.display_lyrics_with_timing(lyrics, song['uri'])
                    return
                else:
                    print("Sorry, the requested song was not found.")
                    return

            case 3:
                os.system('cls')
                if not self._songs_played:
                    print("No songs yet.")
                    os.system('pause')
                    return
                table_data = [(song['frequency'], song['song_name'], song['duration']) for song in sorted(self._songs_played, key=lambda song: int(song['frequency']), reverse=True)]
                songs = colored(self.figlet.renderText("Receiptify"), color='green')
                print(songs)
                
                print(tabulate(table_data, headers=["Qty", "Songs You Listen", ""], tablefmt="grid"))
                os.system('pause')
                return
            
            case 4:
                os.system('cls')
                self.figlet = Figlet(font='small')

                # saved pdf receiptify
                print(colored(self.figlet.renderText("THIS IS VSpotify"), color='red'))
                print(colored("Irwen Fronda - Programmer", color='light_red'))
                
                #save to songs_record.csv
                save(self.get_song_list())
                sys.exit(0)


#It should have 3 other function to meet requirements
def retrieve(spotify):
    _songs_played = spotify.get_song_list()
    try:    
        with open("songs_record.csv", 'r') as file:
            reader = csv.DictReader(file, fieldnames=["frequency", "song_name", "duration"])
            next(reader)

            if not any(reader):
                raise StopIteration("No records yet...")

            file.seek(0)
            next(reader)
        
            for line in reader:
                song_name = line['song_name']
                freq = int(line['frequency'])
                duration = line['duration']
                
                flag_found = False
                for song in _songs_played:
                    if song['song_name'] == song_name:
                        song['frequency'] += freq
                        flag_found = True
                        break
                if not flag_found:
                    _songs_played.append({"frequency" : freq, "song_name" : song_name, "duration": duration})                
    except StopIteration:
        print("No records yet...")


def save(spotify):
    # _songs_played = spotify.get_song_list()
    try:
        with open("songs_record.csv", 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["frequency", "song_name", "duration"])
            writer.writeheader()
            for song in spotify:
                writer.writerow({"song_name" : song['song_name'], "frequency" : song['frequency'], "duration" : song['duration']})
    except Exception as e:
        print(f"Error in saving list of songs: {e}")
        return


def say_song(phrase):
    engine = pyttsx3.init()
    engine.say(phrase)
    engine.runAndWait()


def main():
    spotify = VSpotify.get()
    retrieve(spotify)
    while True: 
        spotify.music_player(spotify.dashboard())
    



if __name__ == "__main__":
    main()