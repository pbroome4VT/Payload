#!/usr/bin/env python3
import time
import signal
import sys
import os
from Gps import gps
from Imu import imu
from Telemetry import telemetry
from Battery import battery
from Sound import sound
from Sound import song
from Sound.Speaker import speaker 
from Timer import timer
import helper as h
#----------------------------------------------------------
#constants
TELEMETRY_DELTA_T = 3.0       #(seconds)  period at which data is transmitted
SENSOR_DELTA_T = 1.0  
STDOUT_DELTA_T = 10.0          #(second)   period at which data is output to console
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

stdoutNum = 0
noFixCtr = 0

def fsm():
    global telemetryTimer
    global stdoutTimer
    
    #print("FSM called")
    timer.Timer.update()    #update all timers
    if(telemetryTimer.is_expired()):
        pass
        global noFixCtr
        msg = ""
        if(gps.has_fix()):
            noFixCtr = 0
            msg = gps.get_position_str()
        else:
            msg = "no fix: " + str(noFixCtr)
            noFixCtr = noFixCtr + 1
        telemetry.transmit(msg)
        print("SENT: " + msg)
        telemetryTimer.reset()
    if(sensorTimer.is_expired()):
        pass
        gps.gps()
        imu.imu()
        telemetry.telemetry()
        sensorTimer.reset()
    if(stdoutTimer.is_expired()):
        pass
        global stdoutNum
        print("-------------------------------")
        print("OUTPUT #" + str(stdoutNum))
        print("Position:  " + gps.get_position_str())
        print("Num Satelites:  " + str(gps.get_num_satelites()))
        print("gps antenna:  " + gps.get_antenna_str())
        print("Temperature:  " + str(imu.get_temperature()))
        print("dps<x,y,z>:  " + str(imu.get_degrees_per_second()))
        print("accel<x,y,z>g's:  " + str(imu.get_acceleration()))
        print("battery voltage:  " + str(round(battery.get_voltage(), 3)) + "V")
        print("------------------------------")
        stdoutNum = stdoutNum + 1
        stdoutTimer.reset()
    sound.sound()

def run():
    print("Run called")
    setup()
    gps.initialize()
    imu.initialize()
    telemetry.initialize()
    battery.initialize()
    sound.initialize()
    sound.play_song(sound.startupSound)
    while 1:
        fsm()
    



if __name__ == "__main__":
    run()
