from Sound.Speaker import speaker
import Sound.constants as c
from Sound import song
import time

songTimer = None
songEn = 0
currSong = None

def initialize():
    global songTimer
    global songEn
    songEn = 0
    if(not speaker.is_initialized()):
        speaker.initialize()

def destroy():
    speaker.disable()

def play_song(s):
    global songEn
    global currSong
    currSong = s
    songEn = 1
    currSong.start()

def stop_song():
    global songEn
    songEn = 0
    speaker.disable()

def sound():
    global songEn
    global currSong
    if(songEn):
        changedNote = currSong.update()
        if(not currSong.song_over()):
            if(changedNote):
                speaker.set_frequency(1)
                time.sleep(0.01)
                speaker.set_frequency(currSong.current_note())
        else:
            stop_song()


