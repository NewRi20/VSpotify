VSpotify

Video Demo:  

Description:

VSpotify is a Python-based music player that integrates with the Spotify and Genius APIs to provide an enhanced music streaming experience. It allows users to search for songs, play random tracks from their favorite artists, display synchronized lyrics, and generate a "VReceiptify" of their most-played songs. The program features voice feedback and a command-line dashboard for seamless interaction.

Features:

Play Songs: Search for and play specific songs or random tracks by an artist.

Lyrics Display: Fetch and display lyrics in sync with playback.

Playback Control: Detects song state (playing, paused, stopped) and adjusts lyrics display accordingly.

History Tracking: Keeps track of played songs and their frequency.

VReceiptify: Generates a summary of the most listened-to songs in a structured table format.

Voice Announcements: Announces the currently playing song.

Persistent Storage: Saves song history to a CSV file for later retrieval.

Installation & Setup:

Clone the repository:

git clone <repository-url>
cd VSpotify

Install the required dependencies:

pip install spotipy lyricsgenius pyttsx3 tabulate termcolor keyboard pyfiglet

Set up API credentials:

Obtain API keys from Spotify Developer and Genius API.

Replace the placeholders in project.py with your Spotify Client ID, Client Secret, and Genius Access Token.

Usage:

Run the script using:

python project.py

Once running, the program will present a dashboard with options:

(1) Search a song – Play a specific song by an artist.

(2) Choose an artist to listen – Play a random song by a chosen artist.

(3) Print VReceiptify – View a summary of listened-to songs.

(4) Exit – Save data and exit.

Controls:

Press q while viewing lyrics to return to the dashboard.

The program automatically detects when a song is paused or stopped.

Notes:

Ensure you are logged into Spotify on your browser for OAuth authentication.

The program requires an active internet connection to fetch data.

License:

This project is open-source and available under the MIT License.

Author:

Irwen Fronda

This was CS50!