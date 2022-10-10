import os
import Adafruit_BBIO.PWM as pwm
import Piezzo.constants as c


#---------------------------------------
#global vars
dutyCycle = 50      #%
frequency = 600
enabled = 0
initialized = False


def initialize_Env():
    pass

def initialize_Piezzo():
    os.system("config-pin p9.14 pwm > /dev/null")
    global initialized
    initialized = True


def set_frequency(newFrequency):
    global intialized
    if(initialized):
        global frequency
        if(newFrequency != frequency):
            enable()
            pwm.set_frequency(c.PIEZZO_CHANNEL, newFrequency)
            frequency = newFrequency

def enable():
    global initialized
    if (initialized):
        pwm.start(c.PIEZZO_CHANNEL, dutyCycle, frequency, polarity = 0)

def disable():
    global initialized
    if(initialized):
        pwm.stop(c.PIEZZO_CHANNEL)
