#!/usr/bin/python
# daemon.py
"""
Python Daemon class
Original Recipe from http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/
"""
import sys, os, time, atexit

import signal
from signal import SIGTERM 

import logging
log = logging.getLogger(__name__)

class Daemon(object):
    """
    A generic daemon class.
    
    Usage: subclass the Daemon class and override the run() method
    """
    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
    
    def daemonize(self):
        """
        do the UNIX double-fork magic, see Stevens' "Advanced 
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        log.info('DAEMONIZING')
        try: 
            pid = os.fork() 
            if pid > 0:
                # exit first parent
                sys.exit(0) 
        except OSError, e: 
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)
    
        # decouple from parent environment
        os.chdir("/") 
        os.setsid() 
        os.umask(0) 
    
        # do second fork
        try: 
            pid = os.fork() 
            if pid > 0:
                # exit from second parent
                sys.exit(0) 
        except OSError, e: 
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1) 
    
        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
    
        # write pidfile
        pid = str(os.getpid())
        file(self.pidfile,'w+').write("%s\n" % pid)

        # register a function to clean up
        # pid file when program exits
        atexit.register(self.delpid)
    
    def delpid(self):
        log.info("stopping and removing pid")
        os.remove(self.pidfile)

    def start(self):
        """
        Start the daemon
        """
        # Check for a pidfile to see if the daemon already runs
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
    
        if pid:
            message = "pidfile %s already exist. Daemon already running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)
        
        # Start the daemon
        self.daemonize()
        self.run()

    def status(self):
        """
        Query status of the daemon
        """
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError, err:
            pid = None

        try:
            procfile = file("/proc/%s/status" % pid, 'r')
            procfile.close()
        except IOError:
            sys.stdout.write("there is not a process with the PID specified in %s\n" % self.pidfile)
            sys.exit(0)
        except TypeError:
            sys.stdout.write("pidfile %s does not exist\n" % self.pidfile)
            sys.exit(0)

        sys.stdout.write("the process with the PID %d is running\n" % pid)

    def stop(self):
        """
        Stop the daemon
        """
        # Get the pid from the pidfile
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError, err:
            log.info("%s is stopped" % sys.argv[0])
            pid = None
    
        if not pid:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return # not an error in a restart

        log.info("going to stop process %s" % pid)
        # Try killing the daemon process    
        try:
            os.kill(pid, SIGTERM)
            time.sleep(1)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    log.error("removing pidfile since there is not a process")
                    os.remove(self.pidfile)
                    pass
            else:
                log.error("error while sending SIGTERM: %s" % err)
                print str(err)
                sys.exit(1)

    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.start()

    def run(self):
        """
        You should override this method when you subclass Daemon. It will be called after the process has been
        daemonized by start() or restart().
        """
