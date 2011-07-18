#!/usr/bin/env python
import sys, time
from lib.daemon import Daemon

import logging
log = logging.getLogger(__name__)

from datetime import datetime

class MyDaemon(Daemon):
    def run(self):
        while True:
            log.info('TOP %s', datetime.now())
            time.sleep(60)
            log.info('ROLLING %s', datetime.now())
