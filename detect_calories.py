import sys
import time
from barcode_scanner import BarcodeScanner
from usbscale import Scale

if __name__ == "__main__":
	scanner = BarcodeScanner()
	try:
	  while 1:
		print 'reading next'
		print scanner.read_next_barcode()
	except KeyboardInterrupt:
	  print 'Exiting...'
	  sys.exit(0)



