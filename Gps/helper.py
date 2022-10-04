import os										#For checking if data directory exists yet or not
import Adafruit_BBIO.UART as UART		        #To configure the multiplexed uart pins on beaglebone
import serial									#for managing uart serial connections
import math										#need modf()
import time
import re                                       #regexp for tokenizing sentences

import Gps.constants as c
from Gps.svDataClassFile import SvData

#gps module global constants
#-------------
#files
logFile = None              #copy of stdout
rawFile = None              #logs raw transmissions between gps module
coordsFile = None           #logs parsed lattitude, longitude, and altitude data
#--------------
#global variables
#general
gps = None                      #serial gps object
led = 0
#-------------------------------------------
#pgtop sentence status vars
externalAntennaEnabled=None   #boolean of whether gps is using external or internal antenna
#-------------------------------------------
#gga sentence status vars
gpsHasFix = False               #boolean of whether gps has locked on location
currentLatitude = None          #most recent latitude fix reading or None if a fix hasnt occured yet
currentLongitude = None         #most recent longitude fix reading or None if a fix hasnt occured yet
currentAltitude = None          #most recent altitude fix reading or None if a fix hasnt occured yet
#-------------------------------------------
#gsa sentence status vars
#most recent horizontal dillution of precision measurement. (How accurately the space vehicles are able to track the antenna)
#hdop < 5.0 is descent   hdop < 1.0 is amazing
currentHDOP = None              
#-------------------------------------------
#gsv sentence status vars
#TODO breakout the parse_gsv() into some global status vars on number of sv's and there snrs. might need a python object
#each space vehicle in gsv sentence gets unique "Satelite id" number. For gnss satelites this is equivaltent to the prn number
#for SBAS and other satelites there are some offsets. long story short the gsv sentence outputs unique number between [1, 96] to identify satelite
#this array will index these id's and leave index 0 as None
spaceVehiclesData = [None] * 97 
#------------------------------------------------------------------------------------

#prints to stdout and a log file
def gps_print(string):
    print(string)
    timestamp = time.strftime("%b_%d_%H:%M:%S")
    logFile.write(timestamp + "\t"+ string + "\n")
    logFile.flush()

#function converts a string in "ddmm.mmmm..." to "ddd.ddddddd" format
#param coord: string in "ddmm.mmmm..." format
#param dir: the direction 'N', 'S', 'E', 'W'
#return string in  "ddd.ddddddd" format (note: output is truncated to 7 decimal places)
def degMinSec_to_decimaldeg(coord, dir):
    coord = float(coord)
    if dir == 'N' or dir == 'E':
        dir = 1
    else:
        dir = -1
    coord = coord/100									#dd.mmmmmm
    coord = math.modf(coord)						#(0.mmmmm, dd.0)
    coord = (coord[1] + coord[0]*100/60)*dir	#dd.0 + mm.mmmm * 60
    return  format(coord, ".7f")		   		#round to 7 decimal points

#function flashes beaglebone status led 1
def flash_led():
    f = open(c.GPS_LED_DIR + "/brightness", "w")
    global led
    if led == 0:
        f.write("1")
        led = 1
    else:
        f.write("0")
        led = 0


def initialize_environment():
    #print("gps_init_env called")

    global logFile
    logFile = open(c.LOG_FILE, "w")

    #create data direcory for logging if it doesnt already exist
    if(not os.path.exists(c.GPS_DATA_DIR)):
        gps_print("Gps.intiialize_environment() data directory doesnt exist")
        gps_print("Gps.initialize_environment() creating Data directory")
        os.mkdir(c.GPS_DATA_DIR)

    #open each gps data file
    global rawFile
    global coordsFile
    rawFile = open(c.RAW_FILE, "w")
    coordsFile = open(c.COORDS_FILE, "w")

    #configure the gps status LED: Disable the trigger and turn off the led
    f = open(c.GPS_LED_DIR + "/trigger", "w")
    f.write("none")
    f.close()
    flash_led()


def read_gps():
    try:
        rawString = gps.readline().decode("UTF-8")
        #if read a full message before timeout
        if (len(rawString) > 0) and (rawString[len(rawString) - 1] == "\n"):
            rawFile.write("<"+rawString)
            rawFile.flush()
            return rawString
    except Exception as e:
        gps_print(str(e))
    return ""

#pmtk command is of the form "$<data>*<checksum>" where checksum is a hexadecimal string
#send this function the <data> portion of this command and it will output the <checksum>
#checksum is calculated by XOR'ing all data bytes
#ex: command_str of "pmtk000,0,0,0,0,0,0,0" returns "2E"
def command_checksum(commandStr):
    checksum = 0
    for i in range(0, len(commandStr)): #loop through each character
        #XOR is commutative & associative so xor current character with running total
        #ord() converts current character to unicode number, which is a type that can be XOR'ed
        checksum = checksum ^ (ord(commandStr[i]))
    return hex(checksum)[2:]   #convert from integer to hex string clipping the leading "0x" of hex format

#sends a command to the gps. These are known as PMTK commands
def send_gps(commandStr, dataStr):
    #create the command to send to gps
    if(dataStr != ""):
        commandStr += "," + dataStr
    commandStr = "$" + commandStr + "*" + command_checksum(commandStr) + "\r\n"
    #send the command
    gps.write(commandStr.encode())
    #log the sent message
    rawFile.write(">" + commandStr)
    rawFile.flush()
    return commandStr.strip()
    
#function initializes the adafruit gps. Enables Beaglebone uart1 pins and creates pyserial
#serial class to this port LOG_FILELOG_FILE
#returns a pyserial serial class connection to the gps
def initialize_GPS():
    #gps_print("initializeGPS() called")
    UART.setup("UART1")
    global gps
    gps = serial.Serial(port="/dev/ttyS1", baudrate=9600, timeout=c.READ_TIMEOUT, write_timeout=0.3)
    if(gps.is_open):
        #gps_print("Gps.intialize_GPS() initializing adafruit gps")
        

        #PMTK_CMD_FULL_COLD_START
        #resets gps to factor defaults
        commandStr = "PMTK104"
        dataStr = ""
        #gps_print(send_gps(commandStr, dataStr))
        #time.sleep(1.5)                                  #sleep is necessary between a full system reset and sending config commands

        #PMTK_API_SET_NMEA_OUTPUT
        #output Global positioning System Fixed Data (GGA, GSA, & GSV) once per position fix
        #GGA : position + fix + time data
        #GSA : contains dilltution of precision -> info about position accuracy and helps determine "signal strength"
        #GSV : satelites in view + signal to noise ratio (SNR)
        commandStr = "PMTK314"
        dataStr = "0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0"
        send_gps(commandStr, dataStr)
        
        
        #PMTK_API_SET_FIX_CTL
        #set gps fix to update once every 1000ms
        commandStr = "PMTK300"
        dataStr = "1000,0,0,0,0"
        send_gps(commandStr, dataStr)
        

        #PMTK_SET_NMEA_UPDATERATE
        #send data once every 1000ms
        commandStr = "PMTK220"
        dataStr = "1000"
        send_gps(commandStr, dataStr)


        #enable gps module output of internal/external antenna connection data
        commandStr = "PGCMD"
        dataStr = "33,1"
        send_gps(commandStr, dataStr)

    else:
        gps_print("Gps.intialize_GPS() serial connection failed")
    return gps

def is_pmtk(rawTokens):
    return (len(rawTokens) > 0 and           #have at least one token 
    len(rawTokens[0]) >= 5 and              #first token is at least 5 chars long
    rawTokens[0][0:5] == "$PMTK")            #first 5 chars are $PMTK

def is_pgtop(rawTokens):
    return (len(rawTokens) > 0 and
    len(rawTokens[0]) >= 6 and
    rawTokens[0][0:7] == "$PGTOP")

def is_gga(rawTokens):
    return (len(rawTokens) > 0 and
    len(rawTokens[0]) >= 6 and
    rawTokens[0][0:7] == "$GPGGA")

def is_gsa(rawTokens):
    return (len(rawTokens) > 0 and
    len(rawTokens[0]) >= 6 and
    rawTokens[0][0:7] == "$GPGSA")

def is_gsv(rawTokens):
    return (len(rawTokens) > 0 and
    len(rawTokens[0]) >= 6 and
    rawTokens[0][0:7] == "$GPGSV")

def parse_pmtk(pmtkTokens):
    gps_print(str(pmtkTokens))

def parse_pgtop(pgtopTokens):
    if(pgtopTokens[1] == "11"):
        antennaStatus = pgtopTokens[2]
        global externalAntennaEnabled
        if(externalAntennaEnabled != antennaStatus):
            if(antennaStatus == "1"):
                gps_print("ACTIVE ANTENNA IS SHORTED")
            elif(antennaStatus == "2"):
                gps_print("SWITCH TO INTERNAL ANTENNA")
            elif(antennaStatus == "3"):
                gps_print("SWITCH TO EXTERNAL ANTENNA")
        externalAntennaEnabled = antennaStatus
            
def parse_gga(gpggaTokens):
    utc_time = gpggaTokens[1]
    lat = gpggaTokens[2]
    ns = gpggaTokens[3] #north/south
    lon = gpggaTokens[4]
    ew = gpggaTokens[5] #east/west
    fix = gpggaTokens[6]
    sats = gpggaTokens[7]
    alt = gpggaTokens[9]
    global gpsHasFix
    if (fix != "0"):							#if packet has data
        global currentLatitude
        global currentLongitude
        global currentAltitude
        gpsHasFix = True
        currentLatitude = degMinSec_to_decimaldeg(lat, ns)
        currentLongitude = degMinSec_to_decimaldeg(lon, ew)
        currentAltitude = alt
        coordsFile.write(currentLatitude +  "," + currentLongitude + "," + currentAltitude + "\n")
        coordsFile.flush()
        #gps_print(currentLatitude + ", " + currentLongitude + ", " + currentAltitude)
    else:
        gpsHasFix = False
        #gps_print("Looking for fix")

def parse_gsa(gpgsaTokens):
    mode1 = gpgsaTokens[1]
    mode2 = gpgsaTokens[2]
    pdop = gpgsaTokens[15]
    hdop = gpgsaTokens[16]
    vdop = gpgsaTokens[17]

    #hdop = horizontal dillution of precision. hdop < 5.0 is good and hdop < 1.0 is amazing
    global currentHDOP
    currentHDOP = hdop
    #gps_print("HDOP = " + hdop) 
    pass

def parse_gsv(gpgsvTokens):
    #gps_print(str(gpgsvTokens))
    numMessages = gpgsvTokens[1]        #gsv sentence might be split into multiple smaller messages. This is the number of messages in this volley of gsv sentences
    msgNumber = int(gpgsvTokens[2])          #this is the message number in the volley of "numMessages"
    global numSpaceVehiclesVisible
    numSpaceVehiclesVisible = gpgsvTokens[3]      #num "space vehicles" visible

    numSvInSentence = int((len(gpgsvTokens) - 5)/4)  #five token fields are unrelated to specific sv. each sv has 4 tokens. therefore this is the number of sv's contained in this sentence
    global spaceVehiclesData
    for i in range (0, numSvInSentence):
        svStartingIndex = 4 + 4*i       #index in sentence of first field of this sv
        satID = int(gpgsvTokens[svStartingIndex])
        elevation = gpgsvTokens[svStartingIndex + 1]
        azimuth = gpgsvTokens[svStartingIndex + 2]
        snr = gpgsvTokens[svStartingIndex + 3]
        if(spaceVehiclesData[satID] == None):
            spaceVehiclesData[satID] = SvData(satID)
        spaceVehiclesData[satID].elevation = elevation
        spaceVehiclesData[satID].azimuth = azimuth
        spaceVehiclesData[satID].snr = snr
           
    
def gps_helper():
    flash_led()
    while(1):
        rawString = read_gps()
        rawTokens = re.split(",|\*", rawString)     #use regexp to tokenize the raw string sentence
        if(is_pmtk(rawTokens)):
            parse_pmtk(rawTokens)       #parse the PMTK fields for data
        elif(is_gga(rawTokens)):		#parse the NMEA fields for a GGA packet
            parse_gga(rawTokens)
        elif(is_gsa(rawTokens)):
            parse_gsa(rawTokens)
        elif(is_gsv(rawTokens)):
            parse_gsv(rawTokens)
        elif(is_pgtop(rawTokens)):
            parse_pgtop(rawTokens)
        elif(len(rawTokens) > 0 and rawTokens[0] != ""):
            gps_print(str(rawTokens))
        else:
            #break the loop if read timout occured
            #gps_print("read timout")
            break
