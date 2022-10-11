#!/usr/bin/env python3
import time
import signal
import sys
import os
from Gps import gps
from Imu import imu
from Telemetry import telemetry
from Piezzo import piezzo
from Timer import timer

#----------------------------------------------------------
#constants
TELEMETRY_DELTA_T = 1.0       #(seconds)  transmit once per second
PIEZZO_DELTA_T = 1.0          #(seconds)  cycle the piezzo buzzer once per second
STDOUT_DELTA_T = 1.0          #(second)   period at which data is output to console
#-----------------------------------------------------------
#global variables
telemetryTimer = None
piezzoTimer = None
stdoutTimer = None


def interrupt_handler(signal, frame):
    print("interrupted")
    piezzo.disable()
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
    global piezzoTimer
    global stdoutTimer
    telemetryTimer = timer.Timer(TELEMETRY_DELTA_T)
    piezzoTimer = timer.Timer(PIEZZO_DELTA_T/2)
    stdoutTimer = timer.Timer(STDOUT_DELTA_T)

stdout_num = 0
def fsm():
    global telemetryTimer
    global piezzoTimer
    global stdoutTimer
    
    #print("FSM called")
    gps.gps()
    imu.imu()
    telemetry.telemetry()
    if(piezzoTimer.is_expired()):
        piezzo.toggle()
        #piezzo.disable()
        piezzoTimer.reset()
    if(telemetryTimer.is_expired()):
        telemetry.transmit("hello world")
        telemetryTimer.reset()
    if(stdoutTimer.is_expired()):
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
    piezzo.initialize()
    while 1:
        fsm()
    



if __name__ == "__main__":
    run()
