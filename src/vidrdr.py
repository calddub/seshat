#!/usr/bin/python3

import numpy as np
import cv2
import time
from datetime import datetime
from threading import Thread
import logging
from seshutils import getts
from vidwrtr import VidWrtr
from motdet import MotDet

#logging.basicConfig(filename='seshat.log',level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)

class VidCap(Thread):

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
	
	def __init__(self,src,nm,ht,wd,fps):
		logging.info( "Initializing VidCap Object"+nm )
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
		self.rotation = 0
		self.framecnt = 0
		self.camname = nm

		#self.vidfeed.set(cv2.CAP_PROP_FRAME_WIDTH,wd)
		self.vidfeed.set(cv2.CAP_PROP_FRAME_WIDTH,wd)
		self.vidfeed.set(cv2.CAP_PROP_FRAME_HEIGHT,ht)
		self.vidfeed.set(cv2.CAP_PROP_FPS,fps)
		self.running = False
		self.warm = False
		
		self.savefeed = False

		ts, strts = getts()
		logging.debug( "Timestamp:"+strts )
		logging.debug( "Capture height="+str(self.capheight)+" width="+str(self.capwidth ))

		## TODO: TEMPORARY!
		#self.vidout = VidWrtr(nm+".mov",640,480,fps)
		self.vidout = VidWrtr(nm,640,480,fps,True)
		self.motdet = MotDet(nm,640,480,5)  # 5 cached entries in motion detector frame buffer

		Thread.__init__(self)

	def start(self):
		# Body
		logging.info( "Start VidCap" )
		self.running = True
		self.vidout.start()
		Thread.start(self)


	def stop(self):
		# Body
		logging.info( "Stopping VidCap" )
		self.vidout.stop()
		self.motdet.close()
		self.running = False

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
				#if( self.rotation > 0 ):
				#	image_center = tuple(np.array(frame.shape[1::-1]) / 2)
				#	rot_mat = cv2.getRotationMatrix2D(image_center, self.rotation, 1.0)
				#	result = cv2.warpAffine(frame, rot_mat, frame.shape[1::-1], flags=cv2.INTER_LINEAR)
				#	frame = result
				# temporary throttle
				#time.sleep(1/10) #100ms

				### TEMPORARY
				self.vidout.write(frame)
				self.motdet.addFrame(frame)


	def getMotDet(self):
		return self.motdet;

