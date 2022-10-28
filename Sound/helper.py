from Sound.Speaker import speaker
import Sound.constants as c
from Sound import song
import time

songTimer = None
songEn = 0
Thunderstruck = song.Song(c.THUNDERSTRUCK_NOTES, c.THUNDERSTRUCK_BPM)
FinalCountdown = song.Song(c.FINAL_COUNTDOWN_NOTES, c.FINAL_COUNTDOWN_BPM)
song = FinalCountdown



def initialize():
    global songTimer
    global songEn
    songEn = 0
    if(not speaker.is_initialized()):
        speaker.initialize()

def destroy():
    speaker.disable()

def play_song():
    global songEn
    global song
    songEn = 1
    song.start()

def stop_song():
    global songEn
    songEn = 0

def sound():
    global songEn
    global song
    if(songEn):
        changedNote = song.update()
        if(changedNote):
            speaker.set_frequency(1)
            time.sleep(0.01)
            speaker.set_frequency(song.current_note())
        


