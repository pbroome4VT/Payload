import Sound.helper as h
import Sound.constants as c
import Sound.song as song

#Songs
thunderstruck = song.Song(c.THUNDERSTRUCK_NOTES, c.THUNDERSTRUCK_BPM,1)
finalCountdown = song.Song(c.FINAL_COUNTDOWN_NOTES, c.FINAL_COUNTDOWN_BPM,1)
happyBirthday = song.Song(c.HAPPY_BIRTHDAY_NOTES, c.HAPPY_BIRTHDAY_BPM,1)
windowsStartup = song.Song(c.WINDOWS_STARTUP_NOTES, c.WINDOWS_STARTUP_BPM, 1)
startupSound = song.Song(c.STARTUP_SOUND_NOTES, c.STARTUP_SOUND_BPM, 1)
beep = song.Song(c.BEEP_NOTES, c.BEEP_BPM, 1)

def initialize():
    h.initialize()

def destroy():
    h.destroy()
    
def play_song(song):
    h.play_song(song)

def stop_song():
    h.stop_song()

def sound():
    h.sound()