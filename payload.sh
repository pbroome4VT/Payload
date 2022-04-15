#!/bin/bash




# Absolute path to Payload directory: Finds the absolute path of the directory containing this file
PAYLOAD_DIR=$(dirname $(readlink -e "$0"))

#cd to payload dir so we can use relative paths to call .py programs
cd "$PAYLOAD_DIR"


# Turn off all beaglebone status LEDS
$PAYLOAD_DIR/Misc/dimLeds.sh


# set PYTHONPATH so python modules can use relative path for imports
export PYTHONPATH="$PAYLOAD_DIR"


#short function to cleanup if the program recieves a SIGTERM signal
_term() {
	echo "Caught SIGTERM signal!"
	$PAYLOAD_DIR/Misc/dimLeds.sh
	kill 0		#terminate all subprocess of this process
}


# starts each software module. If this process is sent SIGTERM, call _term()
(trap _term SIGINT; ./AdafruitGps/gps.py & ./Telemetry/transmitter.py)

