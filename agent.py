from multiprocessing.connection import Client
from array import array

address = ('localhost', 6000)
conn = Client(address)
conn.send('exit')
conn.send('PUT:a,5')
conn.send('GET:a')
msg = conn.recv()
print(msg)
conn.send('close')
conn.close()