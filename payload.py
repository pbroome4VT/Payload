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
#----------------------------------------------------------
#constants
TELEMETRY_DELTA_T = 3.0       #(seconds)  period at which data is transmitted
SENSOR_DELTA_T = 2.0  
STDOUT_DELTA_T = 10.0          #(second)   period at which data is output to console

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


def log(string):
    global logFile
    print(string)
    timestamp = time.strftime("%b_%d_%H:%M:%S")
    logFile.write(timestamp + "\t"+ string + "\n")
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


stdoutNum = 0
noFixCtr = 0

def fsm():
    global telemetryTimer
    global stdoutTimer
    
    #print("FSM called")
    timer.Timer.update()    #update all timers
    if(telemetryTimer.is_expired()):
        if(telemetry.is_initialized()):
            global noFixCtr
            msg = ""
            #send gps coords
            if(gps.has_fix()):
                noFixCtr = 0
                msg = gps.get_position_str()
            else:
                msg = "no fix: " + str(noFixCtr)
                noFixCtr = noFixCtr + 1
            telemetry.transmit(msg)
            log("SENT: " + msg)
            #send battery voltage
            msg = "battery voltage:  " + str(round(battery.get_voltage(), 3)) + "V"
            telemetry.transmit(msg)
            log("SENT: " + msg)
            telemetryTimer.reset()
    if(sensorTimer.is_expired()):
        flash_led()
        gps.gps()
        imu.imu()
        telemetry.telemetry()
        sensorTimer.reset()
    if(stdoutTimer.is_expired()):
        global stdoutNum
        log("-------------------------------")
        log("OUTPUT #" + str(stdoutNum))
        #if(gps.is_connected()):
        #    if(gps.is_initialized()):        
        log("     Position:  " + gps.get_position_str())
        log("     Num Satelites:  " + str(gps.get_num_satelites()))
        log("     gps antenna:  " + gps.get_antenna_str())
        #    else:
        #        print("GPS not initialized")
        #else:
        #    print("GPS NOT CONNECTED")
        log("IMU initialized: " + str(imu.is_initialized()))
        log("     Temperature:  " + str(imu.get_temperature()))
        log("     dps<x,y,z>:  " + str(imu.get_degrees_per_second()))
        log("     accel<x,y,z>g's:  " + str(imu.get_acceleration()))
        log("battery voltage:  " + str(round(battery.get_voltage(), 3)) + "V")
        log("------------------------------")
        stdoutNum = stdoutNum + 1
        stdoutTimer.reset()
    sound.sound()

def run():
    print("Run called")
    initialized = False
    while (not initialized):
        try:
            setup()
            log("main initialized")
            time.sleep(1)
            log("intializing sound")
            sound.initialize()
            log("sound initialized")
            log("initalizing battery")
            battery.initialize()
            log("battery initialized")
            log("initializing gps")
            gps.initialize()
            log("gps initialized")
            initialized = True
        except:
            pass
    gps.gps()
    imu.imu()
    telemetry.telemetry()
    sound.play_song(sound.startupSound)
    while 1:
        fsm()
    



if __name__ == "__main__":
    run()
