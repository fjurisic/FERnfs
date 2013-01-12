#
#   This module is used for probe movement planning
#   and scan control.
#

import thread
from MOTORS2 import Motors

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
            'scanYLenght' not in nfsConf or \
            'stepSize'    not in nfsConf or \
            'stepsPerScanX' not in nfsConf or \
            'stepsPerScanY' not in nfsConf:
                raise Exception("X and Y dimension configuration is insufficient.");
        self.scanXLen = float(nfsConf['scanXLength'])
        self.scanYLen = float(nfsConf['scanYLength'])
        self.stepSize = float(nfsConf['stepSize'])
        self.stepWait = float(nfsConf['stepWait'])
        self.stepX = float(nfsConf['stepsPerScanX'])
        self.stepY = float(nfsConf['stepsPerScanY'])
        self.xOffsetSteps = 0
        self.yOffsetSteps = 0
        self.stopSignal = -1
        self.motors = Motors()
        self.motors.opensercom()
        if 'startingXOffset' in nfsConf:
            offset = float(nfsConf['startingXOffset'])
            while self.xOffsetSteps * self.stepSize < offset:
                self.xOffsetSteps++
        if 'startingYOffset' in nfsConf:
            offset = float(nfsConf['startingYOffset'])
            while self.yOffsetSteps * self.stepSize < offset:
                self.yOffsetSteps++
        # continuing a interrupted scan?
        if 'linesScanned' in nfsConf:
            self.linesScanned = nfsConf['linesScanned']
            self.xOffsetSteps += self.stepX * (int(nfsConf['linesScanned'])+1)
        else:
            self.linesScanned = 0

        if heightMap is not None:
                self.scanZoption = 2
                self.hMap = _calculateApplicableHeightMap(nfsConf)

        elif 'scanZposition' in nfsConf:
            if nfsConf['scanZposition'] is not "fixed":
                self.scanZOption = 1
                self.scanFixedHeight = float(nfsConf['scanZposition'])
        else:
            raise Exception("Insufficient scan heights configuration.")


    def startScan(self):
        """ Starts the scan as a new thread."""
        if self.stopSignal == -1:
            self.stopSignal = 0
            thread.start_new_thread(_startScan, ())
        
    def stopScan(self):
        """ Raises the stop signal. """
        self.stopSignal = 1

    #################### private

    def _startScan():
        """ Starts the scan for real. """
        # move probe to safe height
        # Move required starting offset and note position
        xPosition = self.xOffsetSteps * self.stepSize - float(self.nfsConf['startingXOffset'])
        baseYPosition = self.yOffsetSteps * self.stepSize - float(self.nfsConf['startingYOffset'])
        self.motors.moveXR(self.xOffsetSteps)
        self.motors.moveYF(self.yOffsetSteps)
        sleep(self.stepWait * (self.xOffsetSteps + self.yOffsetSteps))
        
        while True:
            # move probe to initial height
            if self.probeZOption == 1:
                # move to fixed height
            elif self.probeZOption == 2:
                # use hMap
            scanResults = []
            backSteps = 0
            yPosition = baseYPosition
            while True:
                # scan and store result
                if self.probeZOption == 2:
                    # height adjustment may be necessary
                
                yPosition += self.stepY * self.stepSize
                if yPosition > self.scanYLen:
                    break
                if self.stopSignal == 1:
                    self.motors.reset()
                    _completeScan()
                    return
                self.motors.moveYF(self.stepY)
                sleep(self.stepWait * self.stepY)
                backSteps++
            # store result list
            # move probe to safe height 
            self.motors.moveYR(self.stepY * backSteps)
            sleep(self.stepWait * self.stepY * backSteps)
            self.linesScanned++
            xPosition += self.stepX * self.stepSize
            if xPosition > self.scanYlen or self.stopSignal == 1:
                     break
            self.motors.moveXR(self.stepX)
            sleep(self.stepY)
        
        # scan finished or interrupted
        
        self.motors.reset()
        if self.stopSignal != 1:
            self.linesScanned = 0 
        _completeScan()
        return
        
    def _completeScan():
        """ Writes scan configuration to scan result location. """
        scanConf = open(self.nfsConf['scanResultFolder']+"ScanConfig.conf", "w")
        for attribute, value in self.nfsConf.iteritems():
            if attribute is not 'linesScanned':
                scanConf.write(attribute+'='+value+'\n')
        if self.linesScanned != 0:
            scanConf.write('linesScanned='+self.linesScanned)
        scanConf.close()
        if self.callbackFunction != None:
            self.callbackFunction()


    def _calculateApplicableHeightMap(self, nfsConfig, heightMap):
        """
            CURRENTLY NOT SUPPORTED
            Converts the true height map to a map of
            height accessible safely by the probe.
        """
#        self.probeConfig = readConfigFile(nfsConfig['probeConfigFile']) 
#        if self.probeConfig == None:
#            raise Exception('Unable to read probe config file')
#        dx = float(nfsConfig['trueXDimension']) / (nfsConfig['pointXDimension'] - 1)
#        dy = float(nfsConfig['trueYDimension']) / (nfsConfig['pointYDimension'] - 1)
#        ppX = math.ceil(float(probeConfig['dimensionX']) / dx)
#        ppY = math.ceil(float(probeConfig['dimensionY']) / dx)
#        #
#        # TODO allow for second layer of probe dimensions
#        #
#        applicableHeighMap = []
#        for i in range(0, nfsConfig['pointXDimension']):
#            applicableHeightMap.append([])
#            for j in range(0, nfsConfig['pointYDimension']):
#                minX = max(i - ppX, 0)
#                minY = max(j - ppY, 0)
#                maxX = min(i + ppX, nfsConfig['pointXDimension']-1)
#                maxY = min(j + ppY, nfsConfig['pointYDimension']-1)
#                applicableHeightMap[i].append(_findMaxHeight(minX, minY, maxX, maxY, heightMap) + nfsConfig['measureDistance'])
#
#        return applicableHeightMap
#
#    def _findMaxHeight(self, minX, minY, maxX, maxY, heightMap):
#        """Finds the maximum height in a given area of height map"""
#        maxHeight = 0
#        for i in range(minX, maxX+1):
#            for j in range(minY, maxY+1):
#                maxHeight = max(maxHeight, heightMap[i][j])
#        return maxHeight
