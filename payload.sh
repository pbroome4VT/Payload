#!/bin/bash
echo "none">/sys/class/leds/beaglebone:green:usr0/trigger
echo "none">/sys/class/leds/beaglebone:green:usr1/trigger
echo "none">/sys/class/leds/beaglebone:green:usr2/trigger
echo "none">/sys/class/leds/beaglebone:green:usr3/trigger


# Absolute path to Payload directory: Finds the absolute path of the directory containing this file
PAYLOAD_DIR=$(dirname $(readlink -e "$0"))



# set PYTHONPATH so python modules can use relative path for imports
export PYTHONPATH="$PAYLOAD_DIR"


#cd to payload dir so we can use relative paths to call .py programs
cd "$PAYLOAD_DIR"
(trap 'kill 0' SIGINT; ./AdafruitGps/gps.py & ./Telemetry/transmitter.py)

