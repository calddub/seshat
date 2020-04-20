#!/usr/bin/python3

import numpy as np
import cv2
import time
from datetime import datetime
from threading import Thread
import logging
from seshutils import getts
from queue import Queue

#logging.basicConfig(filename='seshat.log',level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)

FRAME_BUFFER = 5

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


	def __init__(self,file,wd,ht,fps):
		logging.info( "Initializing VidWriter Object:"+file )
		self.filename = file
		#self.filename = cv2.VideoCapture(src)

		self.fmwd = wd     # Frame Width
		self.fmht = ht     # Frame Height
		self.fps  = fps    # FPS output rate to file
		self.framecnt = 0  # Current count of frame

		# Set the videocodec for the output file
		#fourcc = cv2.VideoWriter_fourcc(*'VP80')
		fourcc = cv2.VideoWriter_fourcc(*'X264')

		# Writer that stores the video file
		self.vid = cv2.VideoWriter(self.filename, fourcc, fps, (wd,ht))

		# Initializing thread safe FIFO queue to receive frames for writing
		self.frmbuf = Queue(FRAME_BUFFER)   

		self.running = False
		
		ts, strts = getts()
		logging.debug( "VideoWriter initialized, fps="+str(self.fps)+" size=("+str(self.fmwd)+","+str(self.fmht)+")")
		Thread.__init__(self)

	def start(self):
		# Body
		logging.info( "Start VidWrtr" )
		self.running = True
		Thread.start(self)


	def stop(self):
		# Body
		logging.info( "Stopping VidWrtr" )
		self.vid.release()
		self.running = False

	# Add a frame to the write queue...  TODO: If it's full (block or return error?) 
	def write(self,frame):
		#logging.debug( "Writing frame" )
		#self.frmbuf.put(frame)   # Add frame to the processing queue
		self.frmbuf.put_nowait(frame)   # Add frame to the processing queue

	def run(self):
		# Body
		logging.info( "Running VidWrtr" )

		while(self.running):
			try:
				#frame = self.frmbuf.get()   # Retreive frame for writing from queue, block if none
				frame = self.frmbuf.get(False,1)   # Retreive frame for writing from queue, block if none
			except:
				pass
			else:
				self.framecnt += 1
				self.vid.write(frame)
				logging.debug( "Frame Written("+self.filename+"):"+str(self.framecnt))
				self.frmbuf.task_done()
	


