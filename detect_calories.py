import sys
import time
from barcode_scanner import BarcodeScanner
from usbscale import Scale
import requests

if __name__ == "__main__":
	scanner = BarcodeScanner()
	"""url = "http://dweet.io/dweet/for/inf241_barcode_reader?barcode={0}&weight={1}"""
	url = "http://powerful-forest-7649.herokuapp.com/calories?barcode={0}&weight={1}"
	try:
	  while 1:
		print 'reading next'
		barcode = scanner.read_next_barcode()
		scale = Scale()
		weight = scale.get_sampled_weight()
		scale.cleanup()
		print "Barcode : " + str(barcode)
		print "Weight  : " + str(weight)
		requests.get(url.format(barcode, weight))
	except KeyboardInterrupt:
	  print 'Exiting...'
	  scanner.cleanup()
	  sys.exit(0)



