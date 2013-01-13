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
        self.callbackFunction = callbackFunction
        self.scanStatus = 0
        self.scanController = ScanController(nfsConfig, self._callback)

    def startScan(self):
        """ Start your scan! """
        self.scanStatus = 1
        self.scanController.startScan()

    def stopScan(self):
        """ Stop your scan! """
        self.scanController.stopScan()

    def isScanning(self):
        """ Returns True if scanning is currently in progres. """
        if self.scanStatus == 1:
            return True
        else:
            return False

    def _callback(self):
        self.scanStatus = 0
        if self.callbackFunction is not None:
            self.callbackFunction()

cond = threading.Condition()

def rawCallback():
    print "Scan complete!"
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
    scanner.startScan()
    print "Scan started! (type command 'stop' to stop scanning prematurely)"
    while scanner.isScanning() == True:
        command = raw_input(">>")
        if command == "stop":
            scanner.stopScan()
            cond.acquire()
            cond.wait()
            cond.release()
        else:
            print "Unreconized command."

