import time


class Song:
    def __init__(self, notes, bpm, loop):
        self.notes = notes
        self.numNotes = len(notes)
        self.bpm = bpm
        self.loop = loop
        self.index = 0
        self.noteStartTime =  0
        self.beginSong = False   #flag song song has been set to start

    def start(self):
        self.noteStartTime = time.time()
        self.beginSong = True
        pass

    def set_index(self, newIndex):
        self.index = newIndex
    
    def get_index(self):
        return self.index
    
    def set_loop(self, newLoops):
        self.loop = newLoops
        
    def set_song_over(self):
        self.index = -1

    def song_over(self):
        return self.index == -1

    def current_note(self):
        if(not self.song_over()):
            return self.notes[self.index][0]
        else:
            return 0

    def current_note_duration(self):
        if(not self.song_over()):
            return self.notes[self.index][1]
        else:
            return 0

    def advance_note(self):
        if(not self.song_over()):
            self.index = self.index + 1
            self.noteStartTime = time.time()
            if self.loop > 1:
                if(self.index >= self.numNotes):
                    self.index = (self.index)%self.numNotes
                    self.loop = self.loop-1
            else:
                if(self.index >= self.numNotes):
                    self.set_song_over()

    def update(self):
        progressed = False
        if(not self.song_over()):
            currentTime = time.time()
            elapsedTime = currentTime - self.noteStartTime
            noteTime = self.current_note_duration() * 60 / self.bpm #seconds
            while(not self.song_over()   and   elapsedTime > noteTime):
                elapsedTime = elapsedTime - noteTime
                self.advance_note()
                progressed = True
                noteTime = self.current_note_duration() * 60 / self.bpm #seconds
                #print("note " + str(self.index))
                if(noteTime <= 0 ): #in case I do something dumb and make note array of all 0 beat notes
                    break
        return progressed
        

    