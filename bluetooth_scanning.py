from __future__ import print_function
from multiprocessing.connection import Client

import bluetooth
import time

address = ('localhost', 6000)
user1_devices = ['60:6C:66:03:04:ED']

def write_to_file(nearby_devices):
  with open("devices.txt", "w") as f:
    for device in nearby_devices:
      if device in user1_devices:
        print("User 1")

def update_blackboard(nearby_devices):
    conn = Client(address)
    user = "2"
    for device in nearby_devices:
        if device in user1_devices:
            user = "1"
            break
    conn.send('PUT:user,' + str(user))
    conn.send('close')
    conn.close()

while True:
  nearby_devices = bluetooth.discover_devices(lookup_names = False, duration=2)
  print("found %d devices" % len(nearby_devices))
  update_blackboard(nearby_devices)
  time.sleep(0.01)
