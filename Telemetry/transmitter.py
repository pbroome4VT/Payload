#!/usr/bin/env python3

#Author: Paul Broome
#Data 3/13/22
#Description: Reads the gps output file and transmits the contents. This is done using
#	UART2 (tx=p9.21 rx=p9.22) and using a lora transmitter assigned to network #6 with ID #1.
#	to recieve the data, need a lora tranciever on network 6 with ID #2. These choice are all
#	harcoded but easily configuarable

import serial 						#for serial IO
import time							#for sleep()
import os
import Adafruit_BBIO.UART as UART
import AdafruitGps.pylGpsApi as pyl

def flashLed():
	f = open("/sys/class/leds/beaglebone:green:usr0/brightness", "w")
	f.write("0")
	f.flush()
	time.sleep(0.1)
	f.write("1")
	f.close()


def loraReadLine():
	return lora.readline().decode("UTF-8").strip()





flashLed()
UART.setup("UART2") 				#tx = P9.21	rx = p9.22
#setup serial connection on UART2 pins
#/dev/ttyO2 is linux special file for serial UART2 comms
#lora use uart 8N1
lora = serial.Serial("/dev/ttyS2", 115200)
if lora.is_open == False:
	print("lora failed to open")


#assign transmitter to network #6
lora.write("AT+NETWORKID=6\r\n".encode())
print("AT+NETWORKID=6: ", loraReadLine())

#assign transmitter ID #1
lora.write("AT+ADDRESS=1\r\n".encode())
print("AT+ADDRESS=1: ", loraReadLine())

#assign lora parameters
lora.write("AT+PARAMETER=12,4,1,7\r\n".encode())
print("AT+PARAMETER=12,4,1,7: ", loraReadLine())


while True:
	data = pyl.pos()				#"<lat>,<lon>,<alt>"
	if (not data == ""):
		command = "AT+SEND=2," + str(len(data)) + "," + data + "\r\n"
		lora.write(command.encode())
		print(command.strip(),": ", loraReadLine())
		flashLed()
