# Payload 2022

Rocketry@VT
 
Author: Paul Broome

Email: pbroome4@vt.edu

Software for Rocketry@VT Payload 2022. In its current phase, it implements live gps tracking via and Adafruit Ultimate gps connected to UART1. It implements telemetry of this gps data via a lora tranciever connected to UART2. It controls the four Beaglebone onboard Leds to indicate status of the software modules. Lastly, it contains a simple install script which will create a systemd service, allowing the program to run after after boot. This software is created to be scale for the upcoming goal of guided decent and live video transmission.

## Installation Instructions (command line)

### Prerequisites
Some software may need to be installed depending on the linux installation on the beaglebone. The following must be installed on the system to proceed.

git should be installed on the beaglebone by default. This can be confirmed by executing

> git --version

If no version is currently installed, install by running the following command

> sudo apt-get install git
 

python3  should also be installed by default. Again this can be checked by

> python3 --version

and installed by runnning

>sudo apt-get install python3


pip3 must be installed and is likely not installed on the beaglebone by default. To install, run

> sudo apt-get install python3-pip
 
### Payload Software
Install the payload software by entering

>git clone https://github.com/pbroome4VT/Payload.git

>cd Payload

>./install.sh


## Uninstall
To remove the payload software and all its associated files from the beaglebone, run the uninstall.sh script located in the Payload directory (from outside the Payload directory). For example:
>./Payload/uninstall.sh


## Usage
After running install.sh, the program should begin executing immediately and should be configured to begin execution automatically after boot. To disable the software from running after boot, you can run the following command

>systemctl --user disable payload-startup.service

To re-enable the startup functionality, run the following command

>systemctl --user enable payload-startup.service

to start the service(start execution) we can run the following commmand

>systemctl --user start payload-startup.service

Or alternatively, if the service is stopped and we want to see output on the command line, we can run payload.sh located in the Payload directory via

>Payload/payload.sh

