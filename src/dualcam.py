#!/usr/bin/python3

import numpy as np
import cv2
import time
from datetime import datetime
from threading import Thread
import logging
from vidrdr import VidCap
from seshutils import getts

#logging.basicConfig(filename='seshat.log',level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)


# Additional classes???
#   FrameObject #   TrackedObject
#   FrameAnalyzer
#   MothionAnalyzer
#   VidCapWriter


#vcR = VidCap(0,"RCam",640,480,30)
vcR = VidCap(0,"RCam",640,480,15)
vcR.rotation = 180
#vcL = VidCap(2,"LCam",640,480,30)
vcL = VidCap(2,"LCam",640,480,15)
vcL.rotation = 180

#vc2 = VidCap(2,640,480)
#vc3 = VidCap(3,640,480)
vcR.start()
vcL.start()

time.sleep(10)

vcR.stop()
vcL.stop()

