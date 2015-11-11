# import the necessary packages
import imutils
import numpy as np
import argparse
import cv2
import time
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help = "path to the (optional) video file")
args = vars(ap.parse_args())
 
# define the upper and lower boundaries of the HSV pixel
# intensities to be considered 'skin'
lower = np.array([0, 48, 80], dtype = "uint8")
upper = np.array([20, 255, 255], dtype = "uint8")

# if a video path was not supplied, grab the reference
# to the gray
current_channel = 0
try:
	#keep looping over the frames in the video
	while True:
		camera = cv2.VideoCapture(current_channel)
		# grab the current frame
		(grabbed, frame) = camera.read()
		
	 
		# if we are viewing a video and we did not grab a
		# frame, then we have reached the end of the video
		if not grabbed:
			current_channel = (current_channel + 1) % 2
			continue
	 
		# resize the frame, convert it to the HSV color space,
		# and determine the HSV pixel intensities that fall into
		# the speicifed upper and lower boundaries
		frame = imutils.resize(frame, width = 400)
		converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		skinMask = cv2.inRange(converted, lower, upper)
	 
		# apply a series of erosions and dilations to the mask
		# using an elliptical kernel
		kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
		skinMask = cv2.erode(skinMask, kernel, iterations = 2)
		skinMask = cv2.dilate(skinMask, kernel, iterations = 2)
	 
		# blur the mask to help remove noise, then apply the
		# mask to the frame
		skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
		skin = cv2.bitwise_and(frame, frame, mask = skinMask)
	 
		# show the skin in the image along with the mask
		#cv2.imshow("images", np.hstack([frame, skin]))
		cv2.imwrite("/home/neeraj/Dropbox/Camera Uploads/my_img.png", skin)
		time.sleep(1)
		camera.release()
except KeyboardInterrupt:
	camera.release()

cv2.destroyAllWindows()
