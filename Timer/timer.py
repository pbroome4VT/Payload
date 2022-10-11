import time


class Timer:
    
    def __init__(self, elapsed_time):
        self.elapsedTime = elapsed_time
        self.startTime = time.time()
    
    def start(self):
        self.startTime = time.time()

    def reset(self):
        self.start()

    def set_elapsed_time(self, elapsedTime):
        self.elapsedTime = elapsedTime

    def is_expired(self):
        return time.time() - self.startTime > self.elapsedTime