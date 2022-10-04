#!/usr/bin/env python3

#Author: Paul Broome
#Date: 4/14/22
#Desc: Interfaces with Adafruit Ultimate gps connected to Beaglebone UART1 (tx=p9.24 rx=p9.26)




from Gps import helper as h
from Gps import constants as c



def get_latitude():
    return h.currentLatitude
def get_longitude():
    return h.currentLongitude
def get_altitude():
    return h.currentAltitude
def get_hdop():
    return h.currentHDOP

def initialize():
    h.initialize_environment()
    h.initialize_GPS()
    pass

def gps():
    h.gps_helper()
    #print("GPS called")