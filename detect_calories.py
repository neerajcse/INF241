import sys
import time
from barcode_scanner import BarcodeScanner
from usbscale import Scale
import requests

def get_data_from_dashboard(key):
    conn = Client(address)
    conn.send('GET:' + str(key))
    data = conn.recv()
    conn.send('close')
    conn.close()
    return data

def get_weight_from_blackboard():
    return get_data_from_dashboard('weight')
    
def get_user_from_blackboard():
    return "user"

if __name__ == "__main__":
	scanner = BarcodeScanner()
	"""url = "http://dweet.io/dweet/for/inf241_barcode_reader?barcode={0}&weight={1}"""
	url = "http://powerful-forest-7649.herokuapp.com/calories?barcode={0}&weight={1}"
	try:
	  while 1:
		print 'reading next'
		barcode = scanner.read_next_barcode()
        weight = get_weight_from_blackboard()
        user = get_user_from_blackboard()
		print "Barcode : " + str(barcode)
		print "Weight  : " + str(weight)
        print "User    : " + str(user)
		requests.get(url.format(barcode, weight))
	except KeyboardInterrupt:
	  print 'Exiting...'
	  scanner.cleanup()
	  sys.exit(0)