#!/usr/bin/python3

import time
from datetime import datetime


def getts():
	ts = datetime.now()
	strts = ts.strftime('%Y%m%d-%H%M%S.%f')[:-3]

	return ts, strts


