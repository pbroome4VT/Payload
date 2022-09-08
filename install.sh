#!/bin/bash
# AUTHOR: PAUL BROOME
# ROCKETRY@VT- PAYLOAD
# Run after downloading the software.
# script makes the payload script and other scripts executable and creates a startup
# service for the payload software


# Absolute path to Payload directory: Finds the absolute path of the directory containing this file
PAYLOAD_DIR=$(dirname $(readlink -e "$0"))

# CD so we can user relative paths
cd $PAYLOAD_DIR


# make payload script and helper scripts executable
chmod 775 "./payload.sh" "./uninstall.sh" "./Misc/dimLeds.sh"


# install python library dependencies
#pip3 install -r "$PAYLOAD_DIR/Misc/requirements.txt"

# create systemd for user services, if it does not already exist
USER_SERVICE_DIR="$HOME/.config/systemd/user"
mkdir -p "$USER_SERVICE_DIR"


# create softlink to payload startup service
ln -f -s "$PAYLOAD_DIR/Misc/payload-startup.service" "$USER_SERVICE_DIR"


# refresh the systemctl daemon so it will detect the new service
systemctl --user daemon-reload


# enable the startup service. Means this will start at boot
systemctl --user enable payload-startup.service


# start this service.
systemctl --user start payload-startup.service


# this allows the user service to run even when user is not logged in. Without this, service only start after login
sudo loginctl enable-linger $USER
