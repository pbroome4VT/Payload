import Adafruit_BBIO.ADC as adc
import Adafruit_BBIO.GPIO as gpio
import os
from Battery import constants as c
#ain0     =  p9.39     (analog input for reading the voltage)
#gpio_1_1 =  p8.24     (active high enable pin)

enabled = False

def initialize():
    global enabled
    adc.setup()
    gpio.setup(c.ENABLE_PIN, gpio.OUT)
    gpio.output(c.ENABLE_PIN, gpio.HIGH)
    enabled = True

def enable():
    global enabled
    enabled = True
    gpio.output(c.ENABLE_PIN, gpio.HIGH)

def disable():
    global enabled
    enabled = False
    gpio.output(c.ENABLE_PIN, gpio.LOW)

def get_voltage():
    if(enabled):
        return adc.read("AIN0") * c.NORM_TO_BATV_FACTOR 
    else:
        return -1
