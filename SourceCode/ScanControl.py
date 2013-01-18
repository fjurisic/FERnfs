#
#   This module is used for probe movement planning
#   and scan control.
#

import thread
# Change simulator modules with real ones when needed.
from MotorControlSimulator import Motors
from SavingResult import SavingResult
from ProbeControlSimulator import ProbeControl

#
#   Class used to regulate and perform scans
#
class ScanController:
    """Used to control the entire scan."""

    def __init__(self, nfsConf, callbackFunction, heightMap=None):
        """Initialize proper height usage"""
        self.scanZOption = 0
        self.nfsConf = nfsConf
        self.callbackFunction = callbackFunction

        if  'scanXLength' not in nfsConf or \
            'scanYLength' not in nfsConf or \
            'stepSize'    not in nfsConf or \
            'stepsPerScanX' not in nfsConf or \
            'stepsPerScanY' not in nfsConf:
                raise Exception("X and Y dimension configuration is insufficient.");
        self.scanXLen = float(nfsConf['scanXLength'])
        self.scanYLen = float(nfsConf['scanYLength'])
        self.stepSize = float(nfsConf['stepSize'])
        self.stepX = float(nfsConf['stepsPerScanX'])
        self.stepY = float(nfsConf['stepsPerScanY'])
        self.xOffsetSteps = 0
        self.yOffsetSteps = 0
        self.stopSignal = -1
        self.motors = Motors()
        self.probeControl = ProbeControl(nfsConf)
        self.savingResult = SavingResult(nfsConf)
        if 'startingXOffset' in nfsConf:
            offset = float(nfsConf['startingXOffset'])
            while self.xOffsetSteps * self.stepSize < offset:
                self.xOffsetSteps += 1
        if 'startingYOffset' in nfsConf:
            offset = float(nfsConf['startingYOffset'])
            while self.yOffsetSteps * self.stepSize < offset:
                self.yOffsetSteps += 1
        # continuing a interrupted scan?
        if 'linesScanned' in nfsConf:
            self.linesScanned = int(nfsConf['linesScanned'])
            self.yOffsetSteps += self.stepY * self.linesScanned
        else:
            self.linesScanned = 0

        if heightMap is not None:
                self.scanZoption = 2
                self.hMap = _calculateApplicableHeightMap(nfsConf)

        elif 'scanZposition' in nfsConf:
            if nfsConf['scanZposition'] != "fixed":
                self.scanZOption = 1
                self.scanFixedHeight = float(nfsConf['scanZposition'])
        else:
            raise Exception("Insufficient scan heights configuration.")


    def startScan(self):
        """ Starts the scan as a new thread."""
        self.motors.opensercom()
        self.motors.sendconst(int(self.nfsConf['stepWait']))
        self.motors.startpoint()
        if self.stopSignal == -1:
            self.stopSignal = 0
            thread.start_new_thread(self._startScan, ())
        
    def stopScan(self):
        """ Raises the stop signal. """
        self.stopSignal = 1

    #################### private

    def _startScan(self):
        """ Starts the scan for real. """
        # move probe to safe height
        # Move required starting offset and note position
        baseXPosition = self.xOffsetSteps * self.stepSize - float(self.nfsConf['startingXOffset'])
        yPosition = self.yOffsetSteps * self.stepSize - float(self.nfsConf['startingYOffset'])
        self.motors.move(self.xOffsetSteps, self.yOffsetSteps, 0)
        while True:
            # move probe to initial height
            if self.scanZOption == 1:
                # not implemented
                pass 
            elif self.scanZOption == 2:
                # not implemented
                pass
            scanResults = []
            backSteps = 0
            xPosition = baseXPosition
            while True:
                # scan and store result
                print "P: Scanning point"
                scanResult = self.probeControl.scan()
                self.savingResult.setPointResult(scanResult)
                if self.scanZOption == 2:
                    # height adjustment may be necessary
                    pass
                
                xPosition += self.stepX * self.stepSize
                if xPosition > self.scanXLen:
                    break
                if self.stopSignal == 1:
                    self.motors.reset()
                    self._completeScan()
                    return
                self.motors.move(self.stepX, 0, 0)
                backSteps += 1
            # store result list
            print "D: Storing scan results"
            self.savingResult.saveOneLineResult()
            # move probe to safe height 
            self.motors.move(-1 * self.stepX * backSteps, 0, 0)
            self.linesScanned += 1
            yPosition += self.stepY * self.stepSize
            if yPosition > self.scanYLen or self.stopSignal == 1:
                     break
            self.motors.move(0, self.stepY, 0)
        
        # scan finished or interrupted
        
        self.motors.reset()
        self.motors.closesercom()
        if self.stopSignal != 1:
            self.linesScanned = 0 
        self._completeScan()
        return
        
    def _completeScan(self):
        """ Writes scan configuration to scan result location. """
        scanConf = open(self.nfsConf['scanResultFolder']+"ScanConfig.conf", "w")
        for attribute, value in self.nfsConf.iteritems():
            if attribute == 'scanResultFolder':
                scanConf.write(attribute+"=.\n")
            if attribute != 'linesScanned':
                scanConf.write(attribute+'='+value+'\n')
        if self.linesScanned != 0:
            scanConf.write('linesScanned='+str(self.linesScanned)+'\n')
        scanConf.close()
        self.savingResult.waitCompletition()
        if self.callbackFunction is not None:
            self.callbackFunction()

