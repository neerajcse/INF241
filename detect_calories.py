
import sys
import time

fp = open('/dev/hidraw0', 'rb')


def read_next_barcode():
  barcode = ''
  while True:
    if barcode == '':
       time.sleep(0.1)
    buffer = fp.read(8)
    for c in buffer:
      num_val = ord(c)
      if num_val == 40:
        return barcode
      else:
        if num_val > 29 and num_val < 40:
          barcode += str((num_val +1) % 10)
  

def read_weight():
  print "yet to be implemented"


try:
  while 1:
    print 'reading next'
    print read_next_barcode()
except KeyboardInterrupt:
  print 'Exiting...'
  sys.exit(0)




