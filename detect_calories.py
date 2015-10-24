import sys
import time
from barcode_scanner import BarcodeScanner
from usbscale import Scale

if __name__ == "__main__":
	scanner = BarcodeScanner()
	try:
	  while 1:
		print 'reading next'
		barcode = scanner.read_next_barcode()
		scale = Scale()
		weight = scale.get_sampled_weight()
		scale.cleaup()
		print "Barcode : " + str(barcode)
		print "Weight  : " + str(weight)
	except KeyboardInterrupt:
	  print 'Exiting...'
	  scanner.cleanup()
	  sys.exit(0)



