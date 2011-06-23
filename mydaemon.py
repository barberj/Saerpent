#!/usr/bin/env python
import sys, time
from daemon import Daemon

import logging
log = logging.getLogger(__name__)

from datetime import datetime

class MyDaemon(Daemon):
	def run(self):
		while True:
			time.sleep(60)
