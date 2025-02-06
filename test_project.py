import pytest
from project import VSpotify
from project import __init__

#Test empty _song_played
def test_retrieve():
    spotify = VSpotify.get()
    try:
        spotify.retrieve()
    except StopIteration:
        assert False, "It should raise StopIteration error..."
    else:
        assert True
    
def test_save():
    spotify = VSpotify.get()
    try:
        spotify.save()
    except Exception as e:
        assert False, "Error in saving a list of songs..."
    else:
        assert True

def test_get_lyrics():
    spotify = VSpotify.get()
    try:
        spotify.get_lyrics("weeknd", "reminder")
    except Exception as e:
        assert False, "Error in fetching lyrics..."
    else:
        assert True

def test_get_current_song():
    spotify = VSpotify.get()
    try:
        spotify.get_current_song()
    except Exception as e:
        assert False, "Error in getting current song..."
    else:
        assert True

def test__init__():
    try:
        VSpotify.__init__()
    except Exception:
        pass
    else:
        assert False, "It should raises an exception..."
