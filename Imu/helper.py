import Adafruit_BBIO.SPI as SPI
import os
import time
import numpy

import Imu.constants as c
#------------------------------------------
#files
logFile = None
temperatureFile = None
accelerometerFile = None
gyroscopeFile = None
#-------------------------------------------
#global vars
spi = None      #spi interface object
led = 0
#temp data
currentTemperature = 0
#accelerometer data
currentXYZAcceleration = [0]*3
#gyro data
currentXYZDPS = [0] * 3
#--------------------------------------------------

def imu_print(string):
    print(string)
    timestamp = time.strftime("%b_%d_%H:%M:%S")
    logFile.write(timestamp + "\t"+ string + "\n")
    logFile.flush()

def read_register(register):
    byte0 = c.READ_FLAG | register
    data = spi.xfer2([byte0, 0])
    return data

def write_register(register, bytes):
    byte0 = register
    bytes.insert(0, byte0)
    data = spi.xfer2(bytes)
    return data

def is_connected():
    return GPIO.input(c.GPS_GPIO)

def initialize_environment():
    #print("imu initialize_environment() called")

    global logFile
    logFile = open(c.LOG_FILE, "w")

    #create data direcory for logging if it doesnt already exist
    if(not os.path.exists(c.IMU_DATA_DIR)):
        imu_print("Imu.intiialize_environment() data directory doesnt exist")
        imu_print("Ips.initialize_environment() creating Data directory")
        os.mkdir(c.IMU_DATA_DIR)

    #open each imu sensor data file
    global temperatureFile
    temperatureFile = open(c.TEMPERATURE_FILE, "w")
    global accelerometerFile
    accelerometerFile = open(c.ACCELEROMETER_FILE, "w")
    global gyroscopeFile 
    gyroscopeFile = open(c.GYROSCOPE_FILE, "w")
    #configure the imu status LED: Disable the trigger and turn off the led
    f = open(c.IMU_LED_DIR + "/trigger", "w")
    f.write("none")
    f.close()


def initialize_IMU():    
    #configure spi0 pins
    os.system("config-pin p9.17 spi_cs > /dev/null")
    os.system("config-pin p9.18 spi > /dev/null")
    os.system("config-pin p9.21 spi > /dev/null")
    os.system("config-pin p9.22 spi_sclk > /dev/null")

    global spi
    spi = SPI.SPI()
    spi.open(0,0)
    #configure spi device settings based on imu documentation
    spi.bpw = 8             #bits per word. 8?
    spi.cshigh = False      #chip select is active low
    spi.lsbfirst = False    #write bytes msb first 
    spi.mode = 0            #most common spi mode and is supported by the sensor
    spi.msh = 10000000      #max speed in hertz 
    spi.threewire = False   #using four wire spi

    #read and print from the "whoami" register 0x0F.  value is read only 01101011
    #imu_print("whoami = " + hex(spi.xfer2([0b10001111, 0])[1]))

    #configure to imu to ouput acceleration data at 52hz with +-16g's full scale
    dataBytes = [c.CTRL1_XL_ODR_52 | c.CTRL1_XL_FS_16G]
    write_register(c.REG_CTRL1_XL, dataBytes)
    #configure imu to output gyro data at 52hz with 
    dataBytes = [c.CTRL2_G_ODR_52 | c.CTRL2_G_FS_2000]
    write_register(c.REG_CTRL2_G, dataBytes)


def record_temperature():
    #temperature sensor data is 16 bits long, split among two sensor registers
    outTempLow = read_register(c.REG_OUT_TEMP_L)[1]
    outTempHigh = read_register(c.REG_OUT_TEMP_H)[1]
    temperature = outTempHigh<<8 | outTempLow
    temperature = numpy.array([temperature], dtype=numpy.int16)     #convert to 16bit 2's compliment
    tempDegCelsius = c.TEMPERATURE_OFFSET + temperature[0]/c.TEMPERATURE_SENSITIVITY   #convert to celsius
    temperatureFile.write(str(tempDegCelsius) + "\n")       #write temp data to file
    global currentTemperature
    currentTemperature = tempDegCelsius
    #imu_print(str(tempDegCelsius) +  " degrees celsius")    


def record_gyroscope():
    #x-axis gyroscope register data
    outXLow = read_register(c.REG_OUTX_L_G)[1]
    outXHigh = read_register(c.REG_OUTX_H_G)[1]
    xAccel = outXHigh << 8 | outXLow
    #y-axis gyroscope register data
    outYLow = read_register(c.REG_OUTY_L_G)[1]
    outYHigh = read_register(c.REG_OUTY_H_G)[1]
    yAccel = outYHigh << 8 | outYLow
    #z-axis gyroscope register data
    outZLow = read_register(c.REG_OUTZ_L_G)[1]
    outZHigh = read_register(c.REG_OUTZ_H_G)[1]
    zAccel = outZHigh << 8 | outZLow

    xyzGyro = numpy.array([xAccel, yAccel, zAccel], dtype=numpy.int16)
    xyzGyroDPS = [0] * 3
    for i in range(0,2):
        xyzGyroDPS[i] = xyzGyro[i] * c.GYROSCOPE_SENSITIVITY_2000 / 1000
    gyroscopeFile.write(str(xyzGyroDPS) + "\n")
    global currentXYZDPS
    currentXYZDPS = xyzGyroDPS
    #imu_print(str(xyzGyroDPS) + "   deg/s <x,y,z>")

def record_accelerometer():
    #X axis accelerometer register data
    outXLow = read_register(c.REG_OUTX_L_A)[1]
    outXHigh = read_register(c.REG_OUTX_H_A)[1]
    xAccel = outXHigh << 8 | outXLow
    #Y axis accelerometer register data
    outYLow = read_register(c.REG_OUTY_L_A)[1]
    outYHigh = read_register(c.REG_OUTY_H_A)[1]
    yAccel = outYHigh << 8 | outYLow
    #Z axis accelerometer register data
    outZLow = read_register(c.REG_OUTZ_L_A)[1]
    outZHigh = read_register(c.REG_OUTZ_H_A)[1]
    zAccel = outZHigh << 8 | outZLow
    #convert bits to g's
    xyzAccel = numpy.array([xAccel, yAccel, zAccel], dtype=numpy.int16)
    xyzAccelG = [0]*3
    for i in range(0,3):
        xyzAccelG[i] = xyzAccel[i] * c.ACCELEROMETER_SENSITIVTY_16 / 1000
    accelerometerFile.write(str(xyzAccelG)+"\n")
    global currentXYZAcceleration
    currentXYZAcceleration = xyzAccelG
    #imu_print(str(xyzAccelG)  + "      g's <x,y,z>")


def imu():
    #if(is_connected()):
    #    global imuInitialized
    #    if(not imuInitialized):
    #        if(initialize_IMU() != -1):
    #            imuInitialized = True
    #            f = open(c.IMU_LED_DIR + "/brightness", "w")
    #            f.write("1")
    #    else:
    #        imuInitialized = False
    #        f = open(c.IMU_LED_DIR + "/brightness", "w")
    #        f.write("0")

    record_temperature()
    record_accelerometer()
    record_gyroscope()