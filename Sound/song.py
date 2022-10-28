import time

class Song:
    def __init__(self, notes, bpm):
        self.notes = notes
        self.numNotes = len(notes)
        self.bpm = bpm
        self.index = 0
        self.noteStartTime =  0
    
    def start(self):
        self.noteStartTime = time.time()
        pass

    def set_index(self, newIndex):
        self.index = newIndex
    
    def get_index(self):
        return self.index
    
    def current_note(self):
        return self.notes[self.index][0]

    def current_note_duration(self):
        return self.notes[self.index][1]
    
    def advance_note(self):
        self.index = (self.index + 1)%self.numNotes
        self.noteStartTime = time.time()

    def update(self):
        progressed = False
        currentTime = time.time()
        elapsedTime = currentTime - self.noteStartTime
        noteTime = self.current_note_duration() * 60 / self.bpm #seconds
        while(elapsedTime > noteTime):
            elapsedTime = elapsedTime - noteTime
            self.advance_note()
            progressed = True
            noteTime = self.current_note_duration() * 60 / self.bpm #seconds
            print("note " + str(self.index))
            if(noteTime <= 0 ): #in case I do something dumb and make note array of all 0 beat notes
                break
        return progressed
        

    