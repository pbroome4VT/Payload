#Author: Paul Broome
#Data: 3/14/22
#Desciption: short python api/library for the interfacing with the gps data

import os

TELEMETRY_CURRCORD_FILE = os.path.dirname(os.path.abspath(__file__)) + "/Data/currentCoord"


#returns string representation of the current position in "<longitude>,<latitude>,<altiude>"
#format. If an error occurs then an empty string is returned. this function returns the last
#recorded position, even if that position was recorded from a previous gps run.
#Possible error (empty string returned) causes:
#	*The gps program output file has never been created/doesnt have the expected name. This may be
#	caused if the gps program has not yet been run
def pos():
	str = ""
	try:
		f = open(TELEMETRY_CURRCORD_FILE, "r")
		str = f.read().strip()
		f.close()
	except Exception as e:
		print (e)
		str = ""
	return str
