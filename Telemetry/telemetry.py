from Telemetry import helper as h


def initialize():
    h.initialize_environment()
    h.initialize_telemetry()

def transmit(msg):
    return h.transmit(msg)

def telemetry():
    h.telemetry()
