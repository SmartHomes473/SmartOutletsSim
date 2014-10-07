#!/bin/bash

# Set up the Bluetooth serial profile
sudo sdptool browse local | grep "Serial Port" > /dev/null
if [ $? != 0 ]; then
	sudo sdptool add --channel 22 SP
fi

# Listen for incomming connection
if [ ! -e /dev/rfcomm0 ]; then
	sudo rfcomm listen /dev/rfcomm0 22 > /dev/null &
fi

# Launch emultor
./server.py
