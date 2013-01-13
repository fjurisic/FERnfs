#!/usr/bin/env python
#
#   This module encapsulates all NFS functionality.
#

from ScanControl import ScanController
from ConfUtilities import readConfigFile
import threading
import os
import sys

class NearFieldScanner:
    """ Solution for all your near fields """

    def __init__(self, nfsConfig, callbackFunction=None):
        """ Create your own near field scanner """
        # quick and dirty, TODO implement full options
        if not os.path.exists(nfsConfig['scanResultFolder']):
            os.makedirs(nfsConfig['scanResultFolder'])
        self.scanController = ScanController(nfsConfig, callbackFunction)

    def startScan(self):
        """ Start your scan! """
        self.scanController.startScan()

    def stopScan(self):
        """ Stop your scan! """
        self.scanController.stopScan()

cond = threading.Condition()

def rawCallback():
    cond.acquire()
    cond.notifyAll()
    cond.release()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Please provide configuration file."
        sys.exit()
    nfsConfig = readConfigFile(sys.argv[1])
    if nfsConfig is None:
        print "Something is not right with configuration file."
        sys.exit()
    scanner = NearFieldScanner(nfsConfig, rawCallback)
    cond.acquire()
    scanner.startScan()
    cond.wait()
    cond.release()
    


