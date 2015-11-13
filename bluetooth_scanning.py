from __future__ import print_function
from multiprocessing.connection import Client

import bluetooth
import time

address = ('localhost', 6000)

def write_to_file(nearby_devices):
  with open("devices.txt", "w") as f:
    for device in nearby_devices:
      print(device)

def update_blackboard(nearby_devices):
    conn = Client(address)
    conn.send('PUT:devices,' + str(nearby_devices))
    conn.send('close')
    conn.close()

while True:
  nearby_devices = bluetooth.discover_devices(lookup_names = False, duration=2)
  print("found %d devices" % len(nearby_devices))
  write_to_file(nearby_devices)
  time.sleep(0.01)