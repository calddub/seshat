
import numpy as np
import cv2
import time
from datetime import datetime
from threading import Thread
import logging
from seshutils import getts
from vidwrtr import VidWrtr

#logging.basicConfig(filename='seshat.log',level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)

# MotionDetector Object
#   Variables
#     HistoryCnt
#     FrameHistoryArray (of touples) - (rawframe, gsframe, blurframe, XXX)
#     ContourHistory
#     ThresholdValue
#     BlurRange
#     FrameWidth, FrameHeight - Std Frame Size we'll be working with
#   Methods
#     Init
#     CompareFrame( new frame )
#     getContours()   -- Should CompareFrames return contours when adding a frame?
#


class MotDet():

	# Tentatively - allow for reading from either webcam or files
	#   Allow framerate override (especially if working from files)
	#   Candidate parameters for vidcap object: capheight, capwidth, capframerate
	#      frambuffercnt, imagesrc (webcam/file), webcam#?, rotation,???
	#   Should we imbed a storage function to preserve the capture to file
	#      for later use and recreation / debugging purposes? VidCap allows source
	#      direct from webcams OR from files so could use it for predictable testing
	#   For frame buffers, allocate max framebuffer count (10?) and then keep curidx
	#      value that represents the current frame count captured (could be REALLY high)
	#      curidx % maxframecnt = index within the buffer of stored frames
	
	def __init__(self,nm,ht,wd,sz):
		logging.info( "Initializing MoteionDetector Object"+nm )

		self.frameht = ht
		self.framewd = wd
		self.detname = nm
		self.queuesz = sz

		# Standard frame info
		self.framecnt = -1    # Will ++ on each newframe so start with negative framecnt index
		self.rawframe = []    # Raw frame data direct from cam/source
		self.bwframe = []     # Frame translated into BW data
		self.blurframe = []   # Frame after running through initial Gaussian Blur

		# Motion Detection Info
		self.avgframe = []    # Composite average of previous X frames
		self.diffframe = []   # Diff from current frame to composite average
		self.threshframe = [] # Threadshold calc from based on diff
		self.erodeframe = []  # Erosion process to reduce noise
		self.dilateframe = [] # Dilation expands on detected deltas
		self.countours = []   # Calculated contours for motion within frame


		ts, strts = getts()
		logging.debug( "MotionDetector initialized - Timestamp:"+strts )


	def addFrame(self,frame):
		# Temporary conversion steps
		curidx = self.framecnt++%self.queuesz
		prvidx = self.framecnt-1

		# Early in the process will need to allocate data so it can be overwritten later on
		if( self.framecnt < self.queuesz ):
			
			self.rawframe.append(frame)
			self.bwframe.append(frame)
			self.blurframe.append(frame)
			self.avgframe.append(frame)
			self.diffframe.append(frame)
			self.threshframe.append(frame)
			self.erodeframe.append(frame)
			self.dilateframe.append(frame)

		# Leverage gray scale for our image comparison
		self.bwframe[curidx] = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		# Blur/fuzz the image a bit to eliminate background noise
		self.blurframe[curidx] = cv2.GaussianBlur(self.bwframe[curidx], (7, 7), 0)

		# Only can perform frame differences if there was a previous frame
		if( prvidx <= 0 ):
			return

		# Store a weighted average of the previous 5 frames
		self.avgframe[curidx] = avgframe[prvidx].copy().astype("float") # grab previous average
		cv2.accumulateWeighted(self.blurframe[curidx], self.avgframe[curidx], 0.2 )

		# Perform difference of current captured from to (previous | 5frame average)
		self.diffframe[curidx] = cv2.absdiff(blurframe[curidx].astype("uint8"), self.blurframe[prvidx])
		#self.diffframe[curidx] = cv2.absdiff(avgframe[curidx].astype("uint8"), blurframe)

		# Thresholding logic to evaluate the difference between before image and after image
		self.threshframe[curidx] = cv2.threshold(self.diffframe[curidx], 0.5*100, 255, cv2.THRESH_BINARY)[1]
		self.erodeframe[curidx] = cv2.erode(self.threshframe[curidx], None, iterations=2)
		self.dilateframe[curidx] = cv2.erode(self.erodeframe[curidx], None, iterations=2)

		# Pull the contours / differences between frames. Theorietically minimal change == 0
		self.contours[curidx] = cv2.findContours(self.dilateframe[curidx].copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


	def getContours(self):
		pass


