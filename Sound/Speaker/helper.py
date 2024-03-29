import os
import Adafruit_BBIO.PWM as pwm
import Sound.Speaker.constants as c

#---------------------------------------
#global vars
dutyCycle = 50      #%
frequency = 600
enabled = 0
initialized = False


def initialize_Env():
    pass

def initialize_Speaker():
    os.system("config-pin p9.14 pwm > /dev/null")
    global initialized
    initialized = True


def set_frequency(newFrequency):
    global intialized
    if(initialized):
        global frequency
        if(newFrequency != frequency):
            enable()
            pwm.set_frequency(c.SPEAKER_CHANNEL, newFrequency)
            frequency = newFrequency

def enable():
    global initialized
    global enabled
    if (initialized):
        pwm.start(c.SPEAKER_CHANNEL, dutyCycle, frequency, polarity = 0)
        enabled = 1

def disable():
    global initialized
    global enabled
    if(initialized):
        pwm.stop(c.SPEAKER_CHANNEL)
        enabled = 0

def toggle():
    global intialized
    global enabled
    if(enabled == 0):
        enable()
    else:
        disable()