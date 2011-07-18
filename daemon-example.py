#!/usr/bin/env python
import logging
import logging.handlers
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

filehandler = logging.handlers.TimedRotatingFileHandler('/tmp/daemon.log',when='midnight',interval=1,backupCount=9)
formatter = logging.Formatter("%(asctime)-15s %(name)s: %(message)s")
filehandler.setFormatter(formatter)
logger.addHandler(filehandler)

#sysloghandler = logging.handlers.SysLogHandler('ec2-50-16-173-176.compute-1.amazonaws.com',514)
#sysloghandler = logging.handlers.SysLogHandler('10.36.78.6',514)
#sysloghandler = logging.handlers.SysLogHandler('localhost',514)
#sysloghandler = logging.handlers.SysLogHandler('127.0.0.1',514)
# TY!!! http://scottbarnham.com/blog/2008/01/01/sysloghandler-not-writing-to-syslog-with-python-loggin
sysloghandler = logging.handlers.SysLogHandler('/dev/log',514)

sysloghandler.setFormatter(formatter)
logger.addHandler(sysloghandler)

import sys, time
from datetime import datetime

from daemon import Daemon
from mydaemon import MyDaemon


if __name__ == "__main__":
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
