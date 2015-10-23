#!/usr/bin/python
import os
import fcntl
import struct
import time


# inspired by http://kubes.org/src/usbscale.c
def open_hid(dev="/dev/usb/hiddev0"):
    fd = os.open(dev, os.O_RDONLY)
    def _IOC(iodir, iotype, ionr, iosize):
        return (iodir << 30) | (iotype << 8) | (ionr << 0) | (iosize << 16)
    def HIDIOCGNAME(len):
        return _IOC(2, ord("H"), 6, len)
    name = fcntl.ioctl(fd, HIDIOCGNAME(100), " "*100).split("\0",1)[0]

    hiddev_event_fmt = "Ii"
    ev = []
    for _ in range(8):
        ev.append(struct.unpack(hiddev_event_fmt, 
                                os.read(fd, struct.calcsize(hiddev_event_fmt))))
    input_large = ev[6][1]
    input_small = ev[7][1]
    return name, input_small % 256, input_large % 256


def median(l):
  half = len(l) // 2
  l.sort()
  return l[half]


def mean(l):
  return sum(l)/len(l)


def read_scale():
    scale_factor = 2.666666
    print open_hid()
    smalls = []
    larges = []
    for _ in range(5):
        name, small, large = open_hid()
        smalls.append(small)
        larges.append(large)
    base_small = max(smalls)
    base_large = max(larges)
    print "Calibrated..."
    time.sleep(0.5)
    sample = []
    for _ in range(5):
      print "sampling"
      name, small, large = open_hid()
      if large < base_large + 1:
        large = 0
      else:
        large = ((large - (base_large + 1)) * 94) + ((256 - base_small) 
/ scale_factor)
      if large == 0:
        if small >= base_small:
            small = (small - base_small) / scale_factor
        else:
            small = 0
      else:
        small = (small - base_small) / scale_factor
      final = large + small
      sample.append(final)
    print sample
    print max(sample)


if __name__ == "__main__":
  read_scale()
