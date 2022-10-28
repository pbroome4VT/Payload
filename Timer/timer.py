import time


class Timer:
    currentTime = 0     #static time variable
    def __init__(self, elapsed_time):
        self.elapsedTime = elapsed_time
        self.startTime = self.currentTime
    
    @staticmethod
    def update():
        Timer.currentTime = time.time()
    
    def start(self):
        self.startTime = self.currentTime

    def reset(self):
        self.start()

    def set_elapsed_time(self, elapsedTime):
        self.elapsedTime = elapsedTime

    def is_expired(self):
        return self.currentTime - self.startTime > self.elapsedTime