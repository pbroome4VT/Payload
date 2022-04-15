#!/bin/bash
#AUTHOR: PAUL BROOME
#ROCKETRY@VT- PAYLOAD
#Run after downloading. Will set up a startup service so Payload code will run after boot, and begins running the software.


#MUST RUN AS ROOT!



# Absolute path to Payload directory: Finds the absolute path of the directory containing this file
PAYLOAD_DIR=$(dirname $(readlink -e "$0"))


#create softlink to payload startup service
ln -s "$PAYLOAD_DIR/Misc/payload-startup.service" "/etc/systemd/system"


#refresh the systemctl daemon so it will detect the new service
systemctl daemon-reload


#enable the startup service. Means this will start at boot
systemctl enable payload-startup.service


#start this service.
systemctl start payload-startup.service
