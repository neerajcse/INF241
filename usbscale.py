#!/usr/bin/python
import os
import fcntl
import struct
import time

"""
Class which takes care of calibration and sampled weight of an item put
on the usb scale.
"""
class Scale(object):
	"""
	Object for a weighting scale. 
	Classes using this object should only use one method i.e., to get weight of an item put on the scale.
	@link{get_weight} can be used to get the weight.
	"""
	def __init__(self, dev="/dev/usb/hiddev0"):
		self.fd = os.open(dev, os.O_RDONLY)
		self.dev = dev
		self.calibrated = False
		self.name, self.base_small, self.base_large = self.calibrate()
		self.scale_factor = 9.61
	
	"""
	Takes an initial reading and sets that as the relative 0.
	"""
	def calibrate(self):
		smalls = []
		larges = []
		for _ in range(5):
			name, small, large = self.read_hid_usb()
			smalls.append(small)
			larges.append(large)
		base_small = max(smalls)
		base_large = max(larges)
		print "Calibrated..."
		print base_small, base_large
		self.calibrate = True
		return name, base_small, base_large

	""" Gets one sample of weight. """
	def get_weight(self):
		scale_factor = self.scale_factor
		base_large = self.base_large
		base_small = self.base_small
		name, small, large = self.read_hid_usb()
		print small, large
		if large < base_large + 1:
			large = 0
		else:
			large = ((large - (base_large + 1)) * 94) + ((256 - base_small) / scale_factor)
		if large == 0:
			if small >= base_small:
				small = (small - base_small) / scale_factor
			else:
				small = 0
		else:
			small = (small - base_small) / scale_factor
	  	final = large + small
	  	return final
	
	""" Gets @link{self.samples} for weighing and returns the one that has max confidence level. """
	def get_sampled_weight(self):
		sample = []
		for _ in range(5):
			time.sleep(1)
			sample.append(self.get_weight())
		return max(sample)
	 
	""" Reads the usb channel for the scale and converts bytes into readable primitives. """
	def read_hid_usb(self):
		def _IOC(iodir, iotype, ionr, iosize):
			return (iodir << 30) | (iotype << 8) | (ionr << 0) | (iosize << 16)
		def HIDIOCGNAME(len):
			return _IOC(2, ord("H"), 6, len)
		name = fcntl.ioctl(self.fd, HIDIOCGNAME(100), " "*100).split("\0",1)[0]
		hiddev_event_fmt = "Ii"
		ev = []
		for _ in range(8):
			ev.append(struct.unpack(
				hiddev_event_fmt, 
				os.read(self.fd, struct.calcsize(hiddev_event_fmt))))
		input_large = ev[6][1]
		input_small = ev[7][1]
		return name, input_small % 256, input_large % 256

	def cleanup(self):
		os.close(self.fd)

if __name__ == "__main__":
  scale = Scale()
  print(scale.get_sampled_weight())
