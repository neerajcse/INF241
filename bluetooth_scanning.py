from __future__ import print_function
import bluetooth
import time


def write_to_file(nearby_devices):
  with open("devices.txt", "w") as f:
    for device in nearby_devices:
      print(device)
    

while True:
  nearby_devices = bluetooth.discover_devices(lookup_names = False, duration=2)
  print("found %d devices" % len(nearby_devices))
  write_to_file(nearby_devices)
  time.sleep(0.01)