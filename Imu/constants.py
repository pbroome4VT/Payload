import os
import time

IMU_DIR = os.path.dirname(os.path.abspath(__file__))        #IMU module folder
IMU_DATA_DIR = IMU_DIR + "/Data"                #folder to log imu data
#files for logging data
LOG_FILE_TIMESTAMP = time.strftime("%b_%d_%H:%M:%S")
TEMPERATURE_FILE = IMU_DATA_DIR + "/temperature" + LOG_FILE_TIMESTAMP
ACCELEROMETER_FILE = IMU_DATA_DIR + "/accelerometer" + LOG_FILE_TIMESTAMP
GYROSCOPE_FILE = IMU_DATA_DIR + "/gyroscope" + LOG_FILE_TIMESTAMP
LOG_FILE = IMU_DIR + "/log"
IMU_LED_DIR = "/sys/class/leds/beaglebone:green:usr2"


READ_FLAG = 0b10000000

#FIFO_CTRL4_TIMESTAMP_00 = 0b00000000     #dont output timestamps (sensor can output timestamps with resolution of 25 uS)
#FIFO_CTRL4_TEMP_0_HZ = 0b00000000        #0hz temperature sensor update rate
#FIFO_CTRL4_TEMP_1_6_HZ = 0b00010000      #1.6hz temperature sensor update rate
#FIFO_CTRL4_TEMP_12_5_HZ = 0b00100000     #12.5hz temperature sensor update rate
#FIFO_CTRL4_TEMP_52_HZ = 0b00110000       #52hZ temperature sensor update rate
#FIFO_CTRL4_BYPASS_MODE = 0b00000000

#constants related to temperature sensor
TEMPERATURE_OFFSET = 25 # (+-15 deg celsius) #read temperature register of 0 corresponds to 25 deg celsius
TEMPERATURE_SENSITIVITY = 256   #LSB / deg_celsius


#constants related to accelerometer sensor
ACCELEROMETER_SENSITIVTY_16 = 0.488     #mg/LSB  : sensitivity with full scale of +-16g's
ACCELEROMETER_SENSITIVTY_8  = 0.244     #mg/LSB

#constants related to gyroscope sensor
GYROSCOPE_SENSITIVITY_2000 = 70 #mdps/LSB   : angular rate sensitivity with full scale of +-2000dps 

#bitwise or flags for setting REG_CTRL1_XL
CTRL1_XL_ODR_52 = 0b00110000    #accelerometer output data rate of 52 hz
CTRL1_XL_FS_16G = 0b00000100    #accererometer full scale of +- 16 g's


CTRL2_G_ODR_52 = 0b00110000     #gyroscope output data rate
CTRL2_G_FS_1000 = 0b00001000    #gyroscope fulls scale +-1000 dps
CTRL2_G_FS_2000 = 0b00001100    #full scale +-2000 dps


#imu registers
REG_OUT_TEMP_L = 0x20       #temperature lower output byte
REG_OUT_TEMP_H = 0x21       #temperature upper output byte
#REG_FIFO_CTRL4 = 0x0A
REG_CTRL1_XL = 0x10         #accelerometer control register
REG_OUTX_L_A = 0x28         #accelerometer x-axis lower output byte
REG_OUTX_H_A = 0x29         #accelerometer x-axis upper output byte
REG_OUTY_L_A = 0x2A         #accelerometer y-axis lower output byte
REG_OUTY_H_A = 0x2B         #accelerometer y-axis upper output byte
REG_OUTZ_L_A = 0x2C         #accelerometer z-axis lower output byte
REG_OUTZ_H_A = 0x2D         #accelerometer z-axis upper output byte
REG_CTRL2_G = 0x11          #gyroscope control register
REG_OUTX_L_G = 0x22         #gyroscope x-axis lower output byte
REG_OUTX_H_G = 0x23         #gyroscope x-axis upper output byte
REG_OUTY_L_G = 0x24         #gyroscope y-axis lower output byte
REG_OUTY_H_G = 0x25         #gyroscope y-axis upper output byte
REG_OUTZ_L_G = 0x26         #gyroscope z-axis lower output byte
REG_OUTZ_H_G = 0x27         #gyroscope z-axis upper output byte
