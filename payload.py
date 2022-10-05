#!/usr/bin/env python3
import time
from Gps import gps
from Imu import imu

#turn off all onboard leds
def setup():
    file = open("/sys/class/leds/beaglebone:green:usr0/trigger", "w")
    file.write("none")
    file.close()
    file = open("/sys/class/leds/beaglebone:green:usr1/trigger", "w")
    file.write("none")
    file.close()
    file = open("/sys/class/leds/beaglebone:green:usr2/trigger", "w")
    file.write("none")
    file.close()
    file = open("/sys/class/leds/beaglebone:green:usr3/trigger", "w")
    file.write("none")
    file.close()
    file = open("/sys/class/leds/beaglebone:green:usr0/brightness", "w")
    file.write("0")
    file.close()
    file = open("/sys/class/leds/beaglebone:green:usr1/brightness", "w")
    file.write("0")
    file.close()
    file = open("/sys/class/leds/beaglebone:green:usr2/brightness", "w")
    file.write("0")
    file.close()
    file = open("/sys/class/leds/beaglebone:green:usr3/brightness", "w")
    file.write("0")
    file.close()


def fsm():
    #print("FSM called")
    gps.gps()
    imu.imu()
    print(str(gps.get_latitude()) + "  " + str(gps.get_longitude()) + " " + str(gps.get_altitude()))
    #time.sleep(0.25)


def run():
    print("Run called")
    setup()
    gps.initialize()
    imu.initialize()
    while 1:
        fsm()
    



if __name__ == "__main__":
    run()
