#!/usr/bin/env python3

#Author: Paul Broome
#outputs pwm signal to make sound via piezzo buzzer. 
#uses pwm channel pwm1a on pin P9.14


from Piezzo import helper as h
from Piezzo import constants as c


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
    
def initialize():
    h.initialize_Env()
    h.initialize_Piezzo()
    pass


def piezzo():
    h.piezzo()
    pass

