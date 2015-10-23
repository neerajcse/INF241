#!/bin/bash
sudo ifconfig wlan0 up
sudo iwconfig wlan0 essid inf241
sudo dhclient wlan0
curl http://www.google.com 2>&1 >/dev/null
if [ $? -ne 0 ]; then
  echo "Could not connect to internet"
  exit 1
fi
