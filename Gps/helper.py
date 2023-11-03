import os										#For checking if data directory exists yet or not
import Adafruit_BBIO.UART as UART		        #To configure the multiplexed uart pins on beaglebone
import Adafruit_BBIO.GPIO as GPIO               #to read gpio pin to check connection
import serial									#for managing uart serial connections
import math										#need modf()
import time
import re                                       #regexp for tokenizing sentences

import Gps.constants as c
from Gps.svDataClassFile import SvData

#gps module global variables
#-------------
#files
logFile = None              #copy of stdout
rawFile = None              #logs raw transmissions between gps module
coordsFile = None           #logs parsed lattitude, longitude, and altitude data
#--------------
#global variables
#general
gpsInitialized = False
gps = None                      #serial gps object
led = 0
#-------------------------------------------
#pgtop sentence status vars
externalAntennaStatus=None   #boolean of whether gps is using external or internal antenna
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
numSpaceVehiclesVisible = -1
#------------------------------------------------------------------------------------

def log(string):
    timestamp = time.strftime("%b_%d_%H:%M:%S")
    logFile.write(timestamp + "\t"+ string)
    logFile.flush()

#prints to stdout and a log file
def gps_print(string):
    log(string)
    print(string, end="")
    

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




def initialize_environment():
    #print("gps_init_env called")

    global logFile
    logFile = open(c.LOG_FILE, "w")

    #create data direcory for logging if it doesnt already exist
    if(not os.path.exists(c.GPS_DATA_DIR)):
        gps_print("Gps.intiialize_environment() data directory doesnt exist\n")
        gps_print("Gps.initialize_environment() creating Data directory\n")
        os.mkdir(c.GPS_DATA_DIR)

    #open each gps data file
    global rawFile
    global coordsFile
    rawFile = open(c.RAW_FILE, "w")
    coordsFile = open(c.COORDS_FILE, "w")



def read_gps():
    try:
        rawString = gps.readline().decode("UTF-8")
        #if read a full message before timeout
        if (len(rawString) > 0) and (rawString[len(rawString) - 1] == "\n"):
            rawFile.write(">"+rawString)
            rawFile.flush()
            return rawString
    except Exception as e:
        log(str(e))
    return ""

def flush_gps():
    while(read_gps() != ""):
        pass

#splits string at each comma and * character        
def tokenize(rawString):
    return re.split(",|\*", rawString)     #use regexp to tokenize the raw string sentence

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

#checks if the provided "ackStr" is an acknowledge response to the "cmdStr"
#example
# cmd token sent to gps [ $PMTK101, 32, <CR><LF> ] 
# ackToken recieved from gps [ $PMTK001, 101, 0, 33, <CR><LF> ]
def cmd_acknowledge(cmdTokens, ackTokens):
    status = -1
    cmdNum = int( (cmdTokens[0])[5:] )
    if(len(ackTokens) == 4   and   ackTokens[0]=="$PMTK001"   and   int(ackTokens[1])==cmdNum):
        status = int(ackTokens[2])  #the result of the command
    else:
        status = -1         #"ackStr" was not an acknowledgement response for cmdStr. return -1 error
    return status

#sends a command to the gps and checks for an acknowledge. These are known as PMTK commands
# commandStr is a string of form "PMTKXXX" representing the comand to send
# dataStr is comma seperated list of data values for the command
# acknowledge_flag is a flag to enable checking if command was successful
#       0 for no acknowledge necessary
#       1 for must acknowlowedge
#returns an integer:
#   -1 on error. for example if a command was supposed to be acknowledged and was not
#   0 success
def send_gps(commandStr, dataStr, ack=False):
    #create the command to send to gps
    if(dataStr != ""):
        packet = commandStr + "," + dataStr
    else:
        packet = commandStr
    packet = "$" + packet + "*" + command_checksum(packet) + "\r\n"
    
    flush_gps() #flush all buffered gps recieved messages so we can detect an acknowledge packet
    #send the command
    gps.write(packet.encode())
    #log the sent message
    rawFile.write("<" + packet)
    rawFile.flush()
    ret = 0
    if( ack == True ):
        gps.timeout = 0.05  #increase read timeout of gps
        for attempt in range(0, 99): #attempts 100 reads from gps to find acknowledge packet 
            response = read_gps()
            status = cmd_acknowledge(tokenize(packet), tokenize(response))
            if(status != -1):
                break
        if(status == -1):
            log(commandStr + " NOT ACKNOWLEDGED")
            ret = -1
        if(status == 1):
            log(commandStr + " UNSUPPORTED")
            ret = -1
        elif(status == 2):
            log(commandStr + " ACTION FAILED")
            ret = -1
        elif(status == 3):
            log(commandStr + " ACKNOWLEDGED")
            ret = 1
    gps.timeout = c.READ_TIMEOUT # set gps read timeout back to default
    return ret
    


#function initializes the adafruit gps. Enables Beaglebone uart1 pins and creates pyserial
#serial class to this port LOG_FILELOG_FILE
#returns a pyserial serial class connection to the gps
def initialize_GPS():
    status = 0
    UART.setup(c.GPS_UART)
    global gps
    gps = serial.Serial(port=c.GPS_PORT, baudrate=c.GPS_BAUD_RATE, timeout=c.READ_TIMEOUT, write_timeout=c.WRITE_TIMEOUT)
    if(gps.is_open):
        status = send_gps("PMTK000", "", ack = True )
       
        #PMTK_CMD_FULL_COLD_START
        #resets gps to factory defaults
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
        #dataStr = "0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0"
        dataStr = "0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
        status = send_gps(commandStr, dataStr, ack = True)
        if(status == -1):
            return status

        #PMTK_API_SET_FIX_CTL
        #set gps fix to update once every 1000ms
        commandStr = "PMTK300"
        dataStr = "1000,0,0,0,0"
        status = send_gps(commandStr, dataStr, ack = True)
        if(status == -1):
            return status
        

        #PMTK_SET_NMEA_UPDATERATE
        #send data once every 1000ms
        commandStr = "PMTK220"
        dataStr = "1000"
        status = send_gps(commandStr, dataStr, ack = True)
        if(status == -1):
            return status
        
        #enable gps module output of internal/external antenna connection data
        commandStr = "PGCMD"
        dataStr = "33,1"
        status = send_gps(commandStr, dataStr, ack = False)
        if(status == -1):
            return status

        global gpsInitialized
        gpsInitialized = True
        f = open(c.GPS_LED_DIR + "/brightness", "w")
        f.write("1")
    else:
        log("Gps.intialize_GPS() serial connection FAILED")
        return -1
    return 1

def is_pmtk(rawTokens):
    return (len(rawTokens) > 0 and           #have at least one token 
    len(rawTokens[0]) >= 5 and              #first token is at least 5 chars long
    rawTokens[0][0:5] == "$PMTK")            #first 5 chars are $PMTK

def is_pgtop(rawTokens):
    return (len(rawTokens) > 0 and
    len(rawTokens[0]) >= 6 and
    rawTokens[0][0:7] == "$PGTOP")

def is_gga(rawTokens):
    return (len(rawTokens) == 16 and
    len(rawTokens[0]) == 6 and
    rawTokens[0][0:7] == "$GPGGA")

def is_gsa(rawTokens):
    return (len(rawTokens) == 19 and
    len(rawTokens[0]) == 6 and
    rawTokens[0][0:7] == "$GPGSA")

def is_gsv(rawTokens):
    return (len(rawTokens) > 0 and
    len(rawTokens[0]) >= 6 and
    rawTokens[0][0:7] == "$GPGSV")

def parse_pmtk(pmtkTokens):
    gps_print(str(pmtkTokens)+"\n")

def parse_pgtop(pgtopTokens):
    if(pgtopTokens[1] == "11"):
        antennaStatus = int(pgtopTokens[2])
        global  externalAntennaStatus
        if(externalAntennaStatus != antennaStatus):
            if(antennaStatus == c.ANTENNA_SHORTED):
                gps_print("ACTIVE ANTENNA IS SHORTED\n")
            elif(antennaStatus == c.ANTENNA_INTERNAL):
                gps_print("SWITCH TO INTERNAL ANTENNA\n")
            elif(antennaStatus == c.ANTENNA_EXTERNAL):
                gps_print("SWITCH TO EXTERNAL ANTENNA\n")
        externalAntennaStatus = antennaStatus
            
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
    else:
        gpsHasFix = False

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
    currTime = time.time()
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
        spaceVehiclesData[satID].lastComm = currTime
           
    
def gps_helper():
    while(1):
        rawString = read_gps()
        rawTokens = tokenize(rawString)
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
        elif( len(rawTokens) > 0 and rawTokens[0] != ''):
            gps_print(str(rawTokens)+"\n")
        else:
            #break the loop if read timout occured
            break