import os
import Adafruit_BBIO.UART as UART
import serial
import Telemetry.constants as c

tranceiver = None


def initialize_environment():
    pass

def initialize_telemetry():
    os.system("config-pin p8.38 uart > /dev/null")
    os.system("config-pin p8.37 uart > /dev/null")
    #os.system("config-pin p8.31 uart > /dev/null")
    #os.system("config-pin p8.32 uart > /dev/null")
    UART.setup("UART5")
    global tranceiver
    tranceiver = serial.Serial(port="/dev/ttyS5", baudrate=57600, timeout=c.READ_TIMEOUT, write_timeout=0.3)
    if(tranceiver.is_open):
        tranceiver.write(b"ATI")
        pass
    else:
        print("ERROR opening tranceiver serial UART5")



def telemetry():
    global tranceiver
    data = tranceiver.read()
    if(len(data) > 0):
        print(data)