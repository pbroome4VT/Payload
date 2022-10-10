from Telemetry import helper as h
from Telemetry import constants as c


def initialize():
    h.initialize_environment()
    h.initialize_telemetry()

def telemetry():
    h.telemetry()
