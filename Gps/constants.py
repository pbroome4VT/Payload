import os
import time



GPS_DIR = os.path.dirname(os.path.abspath(__file__))        #Gps module folder
GPS_DATA_DIR = GPS_DIR + "/Data"                            #Folder to log Gps data
#files for logging data
LOG_FILE_TIMESTAMP = time.strftime("%b_%d_%H:%M:%S")
RAW_FILE = GPS_DATA_DIR + "/raw" + LOG_FILE_TIMESTAMP             #raw nmea sentences
COORDS_FILE = GPS_DATA_DIR + "/coords" + LOG_FILE_TIMESTAMP         #parsed coordinate data
LOG_FILE = GPS_DIR + "/log"
GPS_LED_DIR = "/sys/class/leds/beaglebone:green:usr1"


READ_TIMEOUT = 50/1000  #seconds
