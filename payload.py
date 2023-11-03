#!/usr/bin/env python3
import time
import signal
import sys
import os
from Gps import gps
from Imu import imu
from Telemetry import telemetry
from Battery import battery
from Timer import timer
#----------------------------------------------------------
#OPTIONS

#constants
TELEMETRY_DELTA_T = 2.0       #(seconds)  period at which data is transmitted
SENSOR_DELTA_T = 1.0            #period at which sensors are queried and have logs updated
STDOUT_DELTA_T = 5.0          #(second)   period at which data is output to console

LOG_FILE_TIMESTAMP = time.strftime("%b_%d_%H:%M:%S")
LOG_DIRECTORY = "Logs"
LOGFILE = LOG_DIRECTORY + "/log"+LOG_FILE_TIMESTAMP

#-----------------------------------------------------------
#global variables
telemetryTimer = None
sensorTimer = None
piezzoTimer = None
stdoutTimer = None
logFile = None

led = 0
stdoutNum = 0
noFixCtr = 0

def log(string):
    print(string, end="")
    timestamp = time.strftime("%b_%d_%H:%M:%S")
    logFile.write(timestamp + "\t"+ string)
    logFile.flush()


def flash_led():
    global led
    if (led == 0):
        f = open("/sys/class/leds/beaglebone:green:usr0" + "/brightness", "w")
        f.write("1")
        led = 1
    else:
        f = open("/sys/class/leds/beaglebone:green:usr0" + "/brightness", "w")
        f.write("0")
        led = 0


#turn off all onboard leds
def setup():
    #disable defualt function of each beaglebone onboard led and turn brightness off so they can be free
    #for modules to communicate with
    os.system("echo \"none\" > /sys/class/leds/beaglebone:green:usr0/trigger")
    os.system("echo \"none\" > /sys/class/leds/beaglebone:green:usr1/trigger")
    os.system("echo \"none\" > /sys/class/leds/beaglebone:green:usr2/trigger")
    os.system("echo \"none\" > /sys/class/leds/beaglebone:green:usr3/trigger")
    os.system("echo \"0\" > /sys/class/leds/beaglebone:green:usr0/brightness")
    os.system("echo \"0\" > /sys/class/leds/beaglebone:green:usr1/brightness")
    os.system("echo \"0\" > /sys/class/leds/beaglebone:green:usr2/brightness")
    os.system("echo \"0\" > /sys/class/leds/beaglebone:green:usr3/brightness")
    #configure global timer variables
    global telemetryTimer
    global sensorTimer
    global stdoutTimer
    global logFile
    telemetryTimer = timer.Timer(TELEMETRY_DELTA_T)
    sensorTimer = timer.Timer(SENSOR_DELTA_T)
    stdoutTimer = timer.Timer(STDOUT_DELTA_T)
    if(not os.path.exists("Logs")):
        os.mkdir(LOG_DIRECTORY)
    logFile = open(LOGFILE, "w")




def fsm():
    global noFixCtr
    timer.Timer.update()
    if ( telemetryTimer.is_expired() ):
        #transmit GPS
        if ( gps.has_fix() ) :
            noFixCtr = 0
            msg = "LAT : " + gps.get_latitude() + "\tLon : " + gps.get_longitude() + "\tAlt : " + gps.get_altitude()
        else : 
            noFixCtr += 1
            msg = "no fix " + str(noFixCtr)
        print("SENT : " + msg)
        telemetry.transmit(msg)
        telemetryTimer.reset()
    if ( sensorTimer.is_expired() ) :
        gps.gps()
        imu.imu()
        sensorTimer.reset()
    if ( stdoutTimer.is_expired() ):
        global stdoutNum
        log("-------------------------------\n")
        log("OUTPUT #" + str(stdoutNum) + "\n")
        log("     " + gps.get_position_str() + "\n")
        log("     Num Satelites:  " + str(gps.get_num_satelites()) + "\n")
        log("     gps antenna:  " + gps.get_antenna_str() + "\n")
        log("IMU initialized: " + str(imu.is_initialized()) + "\n")
        log("     Temperature:  " + str(imu.get_temperature()) + "\n")
        log("     dps<x,y,z>:  " + str(imu.get_degrees_per_second()) + "\n")
        log("     accel<x,y,z>g's:  " + str(imu.get_acceleration()) + "\n")
        log("battery voltage:  " + str(round(battery.get_voltage(), 3)) + "V\n")
        log("------------------------------\n")
        stdoutNum = stdoutNum + 1
        stdoutTimer.reset()

def run():
    print("Run called")
    setup()
    log("initalizing battery")
    battery.initialize()
    log("initializing gps\n")
    gps.initialize()
    log("initializing telemetry\n")
    telemetry.initialize()
    telemetryTimer.start()
    sensorTimer.start()
    stdoutTimer.start()
    while 1:
        fsm()
    



if __name__ == "__main__":
    run()
