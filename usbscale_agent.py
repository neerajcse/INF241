from multiprocessing.connection import Client
from array import array
from usbscale import Scale
import time

address = ('localhost', 6000)

def send_weight_to_blackboard(weight):
    conn = Client(address)
    print("Sending weight :" + str(weight))
    conn.send('PUT:weight,' + str(weight))
    conn.send('close')
    conn.close()

if __name__ == "__main__":
  scale = Scale()
  try:
    history = list()
    while True:
        weight = scale.get_weight()
        #print("Received weight : " + str(weight))
        history.append(weight)
        #print(history)
        if len(history) > 6:
            del history[0]
        max_weight = max(history)
        #print("Max weight : " + str(max_weight))
        send_weight_to_blackboard(max_weight)
        time.sleep(0.1)
  except KeyboardInterrupt:
    print("Exiting...")
  scale.cleanup()
