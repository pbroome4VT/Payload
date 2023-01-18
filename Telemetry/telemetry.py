import Telemetry.helper as h
import Telemetry.constants as c
initialized = False

def is_initialized():
    global initialized
    return initialized
    
def initialize():
    h.initialize_environment()
    h.initialize_telemetry()

def transmit(msg):
    return h.transmit(msg)

def telemetry():
    global initialized
    if (not initialized):
        if (initialize() != -1):
            initialized = True
            f = open(c.TELEMETRY_LED_DIR + "/brightness", "w")
            f.write("1")
    h.telemetry()
