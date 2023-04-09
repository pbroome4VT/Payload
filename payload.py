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
#OPTIONS
LOW_BATTERY_SAFETY_ENABLE = True      #if safety is enabled, beaglebone will beep on battery voltage below threshold1 and shutdown when below threshold2

#constants
TELEMETRY_DELTA_T = 2.0       #(seconds)  period at which data is transmitted
SENSOR_DELTA_T = 1.0            #period at which sensors are queried
STDOUT_DELTA_T = 10.0          #(second)   period at which data is output to console

LOG_FILE_TIMESTAMP = time.strftime("%b_%d_%H:%M:%S")
LOG_DIRECTORY = "Logs"
LOGFILE = LOG_DIRECTORY + "/log"+LOG_FILE_TIMESTAMP

LOW_BATTERY_THRESHOLD1 = 6.8
LOW_BATTERY_THRESHOLD2 = -1
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
    sound.sound()
    if(telemetryTimer.is_expired()):
        if(telemetry.is_initialized()):
            global noFixCtr
            msg = ""
            #send GPS data: "GPS:<lat> <lon> <alt>"
            if(gps.has_fix()):
                noFixCtr = 0
                msg = gps.get_position_str()
            else:
                msg = "no fix " + str(noFixCtr)
                noFixCtr = noFixCtr + 1
            msg = "GPS:" + msg
            telemetry.transmit(msg)
            log("SENT: " + msg)
            #send IMU data:  "IMU:<Acel_x> <Acel_y> <acel_z> <Dps_x> <Dps_y> <Dps_z> <temp>"
            accel = imu.get_acceleration()
            dps = imu.get_degrees_per_second()
            temp = imu.get_temperature()
            msg = "IMU:"+str(accel[0]) + " " +str(accel[1]) +" " + str(accel[2]) + " "+str(dps[0]) + " " + str(dps[1]) + " " + str(dps[2]) + " " + str(temp)
            telemetry.transmit(msg)
            log("SENT: " + msg)
            #send battery data:  "BAT:<voltage>"
            msg = "BAT:"+str(round(battery.get_voltage(), 3))
            telemetry.transmit(msg)
            log("SENT: " + msg)
            telemetryTimer.reset()
    if(sensorTimer.is_expired()):
        flash_led()
        gps.gps()
        imu.imu()
        telemetry.telemetry()
        if(LOW_BATTERY_SAFETY_ENABLE):
            bat = battery.get_voltage()
            if(bat < LOW_BATTERY_THRESHOLD1):
                print("beep")
                sound.play_song(sound.beep)
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
