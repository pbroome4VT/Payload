#!/bin/bash

#locate Payload installation directory relative to this script file
PAYLOAD_DIR=$(dirname $(readlink -e "$0"))/..

#change directory in order to use relative paths for future calls
cd $PAYLOAD_DIR

./Misc/dimLeds.sh
