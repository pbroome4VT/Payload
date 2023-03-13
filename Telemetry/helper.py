import os
import Adafruit_BBIO.UART as UART
import time
import serial
import Telemetry.constants as c

#uart5 rx=p8.38 tx = p8.37
tranceiver = None


def initialize_environment():
    pass

def initialize_telemetry():
    os.system("config-pin p8.38 uart > /dev/null")
    os.system("config-pin p8.37 uart > /dev/null")
    UART.setup("UART5")
    global tranceiver
    tranceiver = serial.Serial(port="/dev/ttyS5", baudrate=c.BAUD_RATE, timeout=c.READ_TIMEOUT, write_timeout=c.WRITE_TIMEOUT)
    if(tranceiver.is_open):
        tranceiver.write(b"+++")
        time.sleep(2)
        tranceiver.write(b"ATI\r")
        time.sleep(0.1)
        tranceiver.write(b"AT&F\r") #reset to factor default
        time.sleep(0.1)
        #tranceiver.write(b"ATS3=111\r") #set register 3 (network id) to 111
        time.sleep(0.1)
        #tranceiver.write(b"ATS9=916,000\r") # set register9 (max freq) to 916 Mhz
        time.sleep(0.1)
        tranceiver.write(b"ATS4=30\r") #set register 4(tx power) to 30db
        time.sleep(0.1)
        tranceiver.write(b"ATS2=64\r")
        time.sleep(0.1)
        tranceiver.write(b"AT&W\r") #write parameters
        time.sleep(0.1)
        tranceiver.write(b"ATZ\r") #reboot modem
        time.sleep(0.3)
    else:
        print("ERROR opening tranceiver serial UART5")


def transmit(msg):
    global tranciever
    msg = str(msg) + "\r\n"
    n = 0
    try:
        n = tranceiver.write(msg.encode('utf-8'))
    except serial.SerialTimeoutException:
        pass
    return n



def telemetry():
    global tranceiver
    data = tranceiver.readline()
    while(len(data)> 0):
        print(data)
        data=tranceiver.readline()