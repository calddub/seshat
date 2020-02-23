#!/usr/bin/python3

import numpy as np
import cv2
import time
from datetime import datetime
from threading import Thread
import logging

#logging.basicConfig(filename='seshat.log',level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)

class VidCap(Thread):

	# Tentatively - allow for reading from either webcam or files
	#   Allow framerate override (especially if working from files)
	#   Candidate parameters for vidcap object: capheight, capwidth, capframerate
	#      frambuffercnt, imagesrc (webcam/file), webcam#?, ???
	#   Should we imbed a storage function to preserve the capture to file
	#      for later use and recreation / debugging purposes? VidCap allows source
	#      direct from webcams OR from files so could use it for predictable testing
	
	#def __init__(self):
	def __init__(self,src,ht,wd,fps):
		# Body
		logging.info( "Initializing VidCap Object" )
		# If src is int (0 or 1 basically) then initialize as webcam, otherwise usr src as filename
		if( isinstance( src, int )):  # This is webcam number
			self.vidfeed = cv2.VideoCapture(src)
			self.vidsrc = src
			self.webcam = True
		else:
			self.vidfeed = cv2.VideoCapture(src)
			self.vidsrc = src
			self.webcam = False

		self.capheight = ht
		self.capwidth = wd

		#self.vidfeed.set(cv2.CAP_PROP_FRAME_WIDTH,wd)
		self.vidfeed.set(cv2.CAP_PROP_FRAME_WIDTH,wd)
		#self.vidfeed.set(cv2.CAP_PROP_FRAME_HEIGHT,ht)
		#self.vidfeed.set(cv2.CAP_PROP_FPS,fps)
		self.running = False
		self.warm = False
		
		self.savefeed = False

		ts, strts = getts()
		logging.debug( "Timestamp:"+strts )
		logging.debug( "Capture height="+str(self.capheight)+" width="+str(self.capwidth ))
		Thread.__init__(self)

	def start(self):
		# Body
		logging.info( "Start VidCap" )
		self.running = True
		Thread.start(self)


	def stop(self):
		# Body
		logging.info( "Stopping VidCap" )
		self.running = False

	def run(self):
		# Body
		logging.info( "Running VidCap" )
		if( self.warm == False ):
			time.sleep(2)

		while(self.running):
			logging.debug( "Capture frame" )
			err,frame = self.vidfeed.read()
			# temporary throtrtle
			time.sleep(1/10) #100ms


# Additional classes???
#   FrameObject #   TrackedObject
#   FrameAnalyzer
#   MothionAnalyzer
#   VidCapWriter

def getts():
	ts = datetime.now()
	strts = ts.strftime('%Y%m%d-%H%M%S.%f')[:-3]

	return ts, strts


vcR = VidCap(0,640,480,30)
vcL = VidCap(2,640,480,30)
#vc2 = VidCap(2,640,480)
#vc3 = VidCap(3,640,480)
vcR.start()
vcL.start()

time.sleep(30)

vcR.stop()
vcL.stop()

