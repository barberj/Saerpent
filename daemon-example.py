#!/usr/bin/env python
import sys, time
from daemon import Daemon
from mydaemon import MyDaemon

import logging
log = logging.getLogger(__name__)

from datetime import datetime

if __name__ == "__main__":
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)
	handler = logging.FileHandler('/tmp/daemon.log')
	formatter = logging.Formatter("%(asctime)-15s %(name)s: %(message)s")
	handler.setFormatter(formatter)
	logger.addHandler(handler)

	daemon = MyDaemon('/tmp/daemon-example.pid')
	if len(sys.argv) == 2:
		logger.info('%s %s',sys.argv[1],sys.argv[0])
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		elif 'status' == sys.argv[1]:
			daemon.status()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		logger.warning('displaying usage')
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)
