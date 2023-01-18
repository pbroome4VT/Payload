#!/usr/bin/env python3

#Author: Paul Broome
#Date: 10/3/22
#Desc: Interfaces with ism330dlc IMU sensor connected via spi
#vin=p9.7     gnd=p9.1      scl=p9.22       sda=p9.18       d0=p9.21        cs=p9.17


from Imu import helper as h
from Imu import constants as c

initialized = False

def get_temperature():
    return h.currentTemperature

def get_acceleration():
    return h.currentXYZAcceleration

def get_degrees_per_second():
    return h.currentXYZDPS

def is_initialized():
    global initialized
    return initialized

def initialize():
    h.initialize_environment()
    return h.initialize_IMU()


def imu():
    global initialized
    if(initialized == False):
        if (initialize() != -1):
            f = open(c.IMU_LED_DIR + "/brightness", "w")
            f.write("1")
            initialized = True
    h.imu()
