#!/usr/bin/env python3
import time
from Gps import gps
from Imu import imu

def fsm():
    #print("FSM called")
    gps.gps()
    imu.imu()
    print(str(gps.get_latitude()) + "  " + str(gps.get_longitude()) + " " + str(gps.get_altitude()))
    #time.sleep(0.25)


def run():
    print("Run called")
    gps.initialize()
    imu.initialize()
    while 1:
        fsm()
    



if __name__ == "__main__":
    run()
