#!/usr/bin/env python3
import time
import signal
import sys
import os
from Gps import gps
from Imu import imu
from Telemetry import telemetry
from Sound import sound 
from Timer import timer
import helper as h
#----------------------------------------------------------
#constants
TELEMETRY_DELTA_T = 50.0       #(seconds)  transmit once per second
SENSOR_DELTA_T = 50.0
PIEZZO_DELTA_T = 50.0          #(seconds)  cycle the piezzo buzzer once per second
STDOUT_DELTA_T = 50.0          #(second)   period at which data is output to console
#-----------------------------------------------------------
#global variables
telemetryTimer = None
sensorTimer = None
piezzoTimer = None
stdoutTimer = None


def interrupt_handler(signal, frame):
    print("SIGINT")
    sound.destroy()
    sys.exit(0)

#turn off all onboard leds
def setup():
    #initialize the SIGTERM handler for gracefully stopping the process
    signal.signal(signal.SIGINT, interrupt_handler)
    #disable defualt function of each beaglebone onboard led and turn brightness off so they can be free
    #for modules to communicate with
    os.system("echo \"none\" > /sys/class/leds/beaglebone:green:usr0/trigger")
    os.system("echo \"none\" > /sys/class/leds/beaglebone:green:usr1/trigger")
    os.system("echo \"none\" > /sys/class/leds/beaglebone:green:usr2/trigger")
    os.system("echo \"0\" > /sys/class/leds/beaglebone:green:usr0/brightness")
    os.system("echo \"0\" > /sys/class/leds/beaglebone:green:usr0/brightness")
    os.system("echo \"0\" > /sys/class/leds/beaglebone:green:usr0/brightness")
    #configure global timer variables
    global telemetryTimer
    global sensorTimer
    global stdoutTimer
    telemetryTimer = timer.Timer(TELEMETRY_DELTA_T)
    sensorTimer = timer.Timer(SENSOR_DELTA_T)
    stdoutTimer = timer.Timer(STDOUT_DELTA_T)

stdout_num = 0
def fsm():
    global telemetryTimer
    global stdoutTimer
    
    #print("FSM called")
    timer.Timer.update()    #update all timers
    sound.sound()
    if(telemetryTimer.is_expired()):
        pass
        telemetry.transmit("hello world")
        telemetryTimer.reset()
    if(sensorTimer.is_expired()):
        pass
        gps.gps()
        imu.imu()
        telemetry.telemetry()
    if(stdoutTimer.is_expired()):
        pass
        global stdout_num
        print("-------------------------------")
        print("OUTPUT #" + str(stdout_num))
        print("Position:  " + str(gps.get_latitude()) + "  " + str(gps.get_longitude()) + " " + str(gps.get_altitude()))
        print("Temperature:  " + str(imu.get_temperature()))
        print("dps<x,y,z>:  " + str(imu.get_degrees_per_second()))
        print("accel<x,y,z>g's:  " + str(imu.get_acceleration()))
        stdout_num = stdout_num + 1
        stdoutTimer.reset()


def run():
    print("Run called")
    setup()
    gps.initialize()
    imu.initialize()
    telemetry.initialize()
    sound.initialize()
    sound.play_song()
    while 1:
        fsm()
    



if __name__ == "__main__":
    run()
