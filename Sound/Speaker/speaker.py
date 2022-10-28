#!/usr/bin/env python3

#Author: Paul Broome
#outputs pwm signal to make sound via piezzo buzzer. 
#uses pwm channel pwm1a on pin P9.14

import Sound.Speaker.constants as c
import Sound.Speaker.helper as h

def enable():
    h.enable()

def disable():
    h.disable()

def toggle():
    h.toggle()
    
def set_frequency(newFrequency):
    h.set_frequency(newFrequency)

def get_frequency():
    return h.frequency

def is_initialized():
    return h.initialized == True

def initialize():
    if(h.initialized == False):
        h.initialize_Env()
        h.initialize_Speaker()


def speaker():
    pass

