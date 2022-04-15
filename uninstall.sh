#!/bin/bash
#Author: Paul Broome

#TODO: uninstall the service, purge all files

#remove the startup.service file that was created to run software after boot
rm "$HOME/.config/systemd/user/payload-startup.service"

#remove all software files
PAYLOAD_DIR=$(dirname $(readlink -e "$0"))
rm -f -R "$PAYLOAD_DIR/*"

