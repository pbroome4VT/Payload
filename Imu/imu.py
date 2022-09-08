#!/usr/bin/env python3
import os
import time
import Adafruit_BBIO.SPI as SPI

def readRegister(spiObj, reg):
	data = spiObj.xfer2([0x80 | reg, 0])
	data = data[1]
	return data

def writeRegister(spiObj, reg, data):
	spiObj.xfer2([reg, data])

def getTemperature(spiObj):
	statusReg = readRegister(spiObj, 0x1E)
	if(statusReg & 0b00000100):
		tempLower = readRegister(spiObj, 0x20)			#lower 8 bits of temperature data
		tempUpper = readRegister(spiObj, 0x21)			#upper 8 bits of temperature data
		return tempUpper << 8 | tempLower
	else:
		print("no new temperature data available")
		return 0

def getAccelerometer(spiObj):
	statusReg = readRegister(spiObj, 0x1E)
	if(statusReg & 0b00000001):
		print("data available")
		xLower = readRegister(spiObj, 0x28)
		xUpper = readRegister(spiObj, 0x29)
		yLower = readRegister(spiObj, 0x2A)
		yUpper = readRegister(spiObj, 0x2B)
		zLower = readRegister(spiObj, 0x2C)
		zUpper = readRegister(spiObj, 0x2D)
		return [xUpper<<8|xLower, yUpper<<8 | yLower, zUpper << 8 | zLower]
	else:
		print("no new accelerometer data")
		return 0

#configure spi0 pins
os.system("config-pin p9.17 spi_cs")
os.system("config-pin p9.18 spi")
os.system("config-pin p9.21 spi")
os.system("config-pin p9.22 spi_sclk")


spi = SPI.SPI()
spi.open(0,0)
spi.msh = 10000000

writeRegister(spi, 0x10, 0b00010000)
while 1:
	data = getTemperature(spi)#getAccelerometer(spi)
	print(data)
	time.sleep(.2)
spi.close()
