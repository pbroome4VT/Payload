#!/usr/bin/env python3

#Author: Paul Broome
#Date: 4/14/22
#Desc: Interfaces with Adafruit Ultimate gps connected to Beaglebone UART4




from Gps import helper as h
from Gps import constants as c

initialized = False


def get_latitude():
    return h.currentLatitude
def get_longitude():
    return h.currentLongitude
def get_altitude():
    return h.currentAltitude
def get_position_str():
    return str(get_latitude()) + " " + str(get_longitude()) + " " + str(get_altitude())
def get_num_satelites():
    return h.numSpaceVehiclesVisible
def get_antenna_str():
    msg = str(None)
    if h.externalAntennaStatus == c.ANTENNA_SHORTED:
        msg = "shorted"
    elif h.externalAntennaStatus ==  c.ANTENNA_INTERNAL:
        msg = "internal"
    elif h.externalAntennaStatus == c.ANTENNA_EXTERNAL:
        msg = "external"
    return msg
def get_hdop():
    return h.currentHDOP
def has_fix():
    return h.gpsHasFix

def is_connected():
    return h.gpsConnected

def is_initialized():
    return h.gpsInitialized



def gps():
    h.gps_helper()