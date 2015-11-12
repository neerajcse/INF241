from multiprocessing.connection import Client
from array import array
from usbscale import Scale
import time

address = ('localhost', 6000)

def send_weight_to_blackboard(weight):
    conn = Client(address)
    conn.send('PUT:weight,' + str(weight))
    conn.send('close')
    conn.close()

if __name__ == "__main__":
  scale = Scale()
  try:
    while True:
        weight = scale.get_weight()
        send_weight_to_blackboard(weight)
        time.sleep(0.5)
  except KeyboardInterrupt:
    print("Exiting...")
  scale.cleanup()
