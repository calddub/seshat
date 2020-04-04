#!/usr/bin/python3

import numpy as np
import cv2
import time
from datetime import datetime
from threading import Thread
import logging
from seshutils import getts

#logging.basicConfig(filename='seshat.log',level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)

class VidWrtr(Thread):

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

	# Need to identify appropriate codec for consumption
	#   vcgencmd codec_enabled VP8 == Enabled by default on RPi4	
	#   vcgencmd codec_enabled H264 == Enabled by default on RPi4	


	def __init__(self,file,ht,wd,fps):
		logging.info( "Initializing VidWriter Object:"+file )
		self.filename = file
		#self.filename = cv2.VideoCapture(src)

		self.capheight = ht
		self.capwidth = wd
		self.framecnt = 0

		# Set the videocodec for the output file
		#fourcc = cv2.VideoWriter_fourcc(*'VP8')
		fourcc = cv2.VideoWriter_fourcc(*'X264')

		# Writer that stores the video file
		vid = cv2.VideoWriter('output.mov',fourcc, fps, (wd,ht))

		self.running = False
		
		ts, strts = getts()
		logging.debug( "VideoWriter initialized, fps="+fps+" size=("+str(self.capheight)+","+str(self.capwidth )+")")
		Thread.__init__(self)

	def start(self):
		# Body
		logging.info( "Start VidWrtr" )
		self.running = True
		Thread.start(self)


	def stop(self):
		# Body
		logging.info( "Stopping VidWrtr" )
		self.running = False

	# Add a frame to the write queue...  TODO: If it's full (block or return error?) 
	def write(self,frame):
		logging.debug( "Writting frame" )

	def run(self):
		# Body
		logging.info( "Running VidCap" )
		if( self.warm == False ):
			time.sleep(2)
			self.warm == True

		while(self.running):
			succ,frame = self.vidfeed.read()
			self.framecnt += 1

			if not succ:
				logging.debug( "Capture frame("+self.camname+"):"+str(self.framecnt) +" err:"+str(succ) )
			else:
				logging.debug( "Capture frame("+self.camname+"):"+str(self.framecnt) +" "+str(frame.shape)+" success:"+str(succ) )

				# Not sure we want to rotate = 2inches additional cam separation worth 10% CPU overhead?
				if( self.rotation > 0 ):
					image_center = tuple(np.array(frame.shape[1::-1]) / 2)
					rot_mat = cv2.getRotationMatrix2D(image_center, self.rotation, 1.0)
					result = cv2.warpAffine(frame, rot_mat, frame.shape[1::-1], flags=cv2.INTER_LINEAR)
					frame = result
				# temporary throttle
				#time.sleep(1/10) #100ms




