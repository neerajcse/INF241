#!/bin/bash
sudo ifconfig wlan0 up
sudo iwconfig wlan0 essid inf241
sudo dhclient wlan0
curl http://www.google.com 2>&1 >/dev/null
if [ $? -ne 0 ]; then
  echo "Could not connect to internet"
  exit 1
fi

# start the blackboard service
sudo python blackboard.py > /dev/null &
if [ $? -ne 0 ]; then
  echo "Could not start the blackboard service"
  exit 1
fi

sudo python usbscale_agent.py > /dev/null &
if [ $? -ne 0 ]; then
  echo "Could not start the usb scale agent"
  exit 1
fi

sudo python detect_calories.py

#TODO: Add a exit hook to kill all python services.

