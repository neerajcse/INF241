from multiprocessing.connection import Listener
from array import array
import sys

address = ('localhost', 6000)
listener = Listener(address)

key_store = {}

try:
    while True:
        try:
            print("Listening for connections...")
            conn = listener.accept()
            print('connection accepted from', listener.last_accepted)
            while True:
                msg = conn.recv()
                # do something with msg
                if msg == 'close':
                    conn.close()
                    break
                if msg == 'exit':
                    listener.close()
                    sys.exit(0)
                if msg.startswith("GET:"):
                    key = msg.split(":")[1].split(",")[0]
                    conn.send(key_store.get(key, ""))
                if msg.startswith("PUT:"):
                    key,value = msg.split(":")[1].split(",")
                    key_store[key] = value
    
        except KeyboardInterrupt:
            print("Exiting...")
            break
except KeyboardInterrupt:
    print("Exiting///")

listener.close()
        