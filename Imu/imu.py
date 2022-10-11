#!/usr/bin/env python3

#Author: Paul Broome
#Date: 10/3/22
#Desc: Interfaces with ism330dlc IMU sensor connected via spi
#vin=p9.7     gnd=p9.1      scl=p9.22       sda=p9.18       d0=p9.21        cs=p9.17


from Imu import helper as h
from Imu import constants as c

def get_temperature():
    return h.currentTemperature

def get_acceleration():
    return h.currentXYZAcceleration

def get_degrees_per_second():
    return h.currentXYZDPS


def initialize():
    h.initialize_environment()
    h.initialize_IMU()


def imu():
    h.imu()
