#!/usr/bin/env python3

#Author: Paul Broome
#Date: 4/14/22
#Desc: Interfaces with Adafruit Ultimate gps connected to Beaglebone UART1 (tx=p9.24 rx=p9.26)


import os										#For checking if data directory exists yet or not
import serial									#for managing uart serial connections
import time										#using sleep and current time to generate log files
import math										#need modf()
import Adafruit_BBIO.UART as UART		#To configure the multiplexed uart pins on beaglebone

GPS_DIR = os.path.dirname(os.path.abspath(__file__))
GPS_DATA_DIR = GPS_DIR + "/Data"

#files for logging data
NMEA_FILE = GPS_DATA_DIR + "/nmea"
COORDS_FILE = GPS_DATA_DIR + "/coords"
TMP_FILE = GPS_DATA_DIR + "/tmp"					#temporary log file
POS_FILE = GPS_DATA_DIR + "/currentCoord"		#logs gps reading
logFile = open(GPS_DIR + "/log", "w")			#copy of stdout

#function flashes beaglebone status led 1
def flashLed():
	f = open("/sys/class/leds/beaglebone:green:usr1/brightness", "w")
	f.write("0")
	f.flush()
	time.sleep(0.1)
	f.write("1")
	f.close()


#splits stdout. prints to normal stdout and to a log file
def Gps_print(string):
	print(string)
	logFile.write(string + "\n")
	logFile.flush()



#function converts a string in "ddmm.mmmm..." to "ddd.ddddddd" format
#param coord: string in "ddmm.mmmm..." format
#param dir: the direction 'N', 'S', 'E', 'W'
#return string in  "ddd.ddddddd" format (note: output is truncated to 7 decimal places)
def nmeaToDecDeg(coord, dir):
	coord = float(coord)
	if dir == 'N' or dir == 'E':
		dir = 1
	else:
		dir = -1
	coord = coord/100									#dd.mmmmmm
	coord = math.modf(coord)						#(0.mmmmm, dd.0)
	coord = (coord[1] + coord[0]*100/60)*dir	#dd.0 + mm.mmmm * 60
	return  format(coord, ".7f")		   		#round to 7 decimal points

#functions initializes the adafruit gps. Enables Beaglebone uart1 pins and creates pyserial
#serial class to this port
#returns a pyserial serial class connection to the gps
def initializeGPS():
	Gps_print("initializeGPS() called")
	UART.setup("UART1")
	gps = serial.Serial("/dev/ttyS1", 9600)
	if(gps.isOpen()):
		Gps_print("intializeGPS() configuring gps")
		#PMTK_API_SET_NMEA_OUTPUT
		#output Global Positioning System Fixed Data (GGA) once per position fix
		gps.write(b"$PMTK314,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*29\r\n")
		#PMTK_API_SET_FIX_CTL
		#set gps fix to update once every 1000ms
		gps.write(b"$PMTK300,1000,0,0,0,0*1C\r\n")
		#PMTK_SET_NMEA_UPDATERATE
		#send data once every 1000ms
		gps.write(b"$PMTK220,1000*1F\r\n")
	else:
		print("intializeGPS() serial connection failed")
	return gps


#creates log file data directory
def initializeEnv():
	Gps_print("intitializeEnv() called")
	#create data direcory for logging if it doenst already exist
	if(not os.path.exists(GPS_DATA_DIR)):
		Gps_print("intiializeEnv() data directory doesnt exist")
		Gps_print("initializeEnv() creating data directory")
		os.mkdir(GPS_DATA_DIR)
	#create/clear the data in POS_FILE
	f = open(POS_FILE, "w")
	f.truncate()
	f.close()
	if(os.path.exists(COORDS_FILE)):
		os.remove(COORDS_FILE)
	if(os.path.exists(NMEA_FILE)):
		os.remove(NMEA_FILE)




#PROGRAM START
initializeEnv()

#create logging files
COORDS_LOG_FILE = COORDS_FILE + str(time.time())
NMEA_LOG_FILE = NMEA_FILE + str(time.time())

#setup serial gps and tranciever connections
gps = initializeGPS()

#record gps transmissions and log to file
nmea_file = open(NMEA_FILE, "w")
nmea_log_file = open(NMEA_LOG_FILE, "w")
coords_file = open(COORDS_FILE, "w")
coords_log_file = open(COORDS_LOG_FILE, "w")
while True:
	try:
		flashLed()
		tmp_file = open(TMP_FILE, 'w')
		nmea_string = gps.readline().decode("UTF-8")
		nmea_file.write(nmea_string)
		nmea_file.flush()
		nmea_log_file.write(nmea_string)
		nmea_log_file.flush()
		nmea_string = nmea_string.split(",")
		if(nmea_string[0] == "$GPGGA"):		#parse the NMEA fields for a GGA packet
			utc_time = nmea_string[1]
			lat = nmea_string[2]
			ns = nmea_string[3] #north/south
			lon = nmea_string[4]
			ew = nmea_string[5] #east/west
			fix = nmea_string[6]
			alt = nmea_string[9]
			if (fix != "0"):							#if packet has data
				lat = nmeaToDecDeg(lat, ns)
				lon = nmeaToDecDeg(lon, ew)
				coords_file.write(lat +  ","+ lon + "," + alt + "\n")
				coords_file.flush()
				coords_log_file.write(lat + "," + lon + "," + alt + "\n")
				coords_log_file.flush()
				tmp_file.write(lat + "," + lon + "," + alt + "\n")
				tmp_file.flush()
				os.replace(TMP_FILE, POS_FILE)
				Gps_print(lat + ", " + lon + ", " + alt)
			else:
				tmp_file.write("-1,-1,-1")
				tmp_file.flush()
				os.replace(TMP_FILE, POS_FILE)
				Gps_print("Looking for fix")
	except Exception as e:
		Gps_print(str(e))
