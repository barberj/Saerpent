#!/usr/bin/env python
# mydaemon.py
"""
Our child daemon class. The work that actually gets done in
the background by a daemon
"""
import sys, time

import logging
log = logging.getLogger(__name__)

import signal
from signal import SIGTERM

from datetime import datetime

from lib.daemon import Daemon

class MyDaemon(Daemon):
    """
    Test implementation of python daemon class 
    including a signal handler.
    """

    def __init__(self,*args,**kwargs):
        # call init for parent
        super(MyDaemon,self).__init__(*args,**kwargs)

        # init stuff particutlar to child
        self.stopping = False

    def set_stop(self,*args,**kwargs):
        """
        Signal handler. When executed we are going
        set stopping to True so daemon can exit
        """

        self.stopping = True
        log.info('[SET_STOP] We are going to stop')

    def is_stopping(self):
        """
        Have we been told to stop?
        """
        return stopping

    def run(self):
        """
        Daemon run method. The actual stuff done
        by the daemon
        """

        # register our signal handler
        signal.signal(SIGTERM, self.set_stop)

        # main work loop
        while not self.is_stopping():
            log.info('TOP %s', datetime.now())
            time.sleep(60)
            log.info('ROLLING %s', datetime.now())

        # SIGTERM receieved so we have exited loop
        # print the final msg
        log.info('STOPPING %s', datetime.now())
