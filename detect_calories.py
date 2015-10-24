
import sys
import time


class BarcodeScanner():
	def __init__(self, channel="/dev/hidraw0"):
		self.fp = open(channel, 'rb')

	def read_next_barcode(self):
		barcode = ''
		while True:
			if barcode == '':
				time.sleep(0.1)
			buffer = self.fp.read(8)
			for c in buffer:
				num_val = ord(c)
				if num_val == 40:
					return barcode
				else:
				if num_val > 29 and num_val < 40:
					barcode += str((num_val +1) % 10)

if __name__ == "__main__":
	scanner = BarcodeScanner()
	try:
	  while 1:
		print 'reading next'
		print scanner.read_next_barcode()
	except KeyboardInterrupt:
	  print 'Exiting...'
	  sys.exit(0)



