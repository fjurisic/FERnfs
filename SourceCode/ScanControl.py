#
#   This module is used for probe movement planning
#   and scan control.
#

from ConfUtilities import readConfigFile

#
#   Class used to regulate and perform scans
#
class ScanController:
    """Used to control the entire scan."""
    
    def __init__(self, nfsCofiguration, heightMap):
        # TODO

    def startScan(self):
        """Starts the scanning process."""
        # TODO

    #################### private

    def _calculateApplicableHeightMap(self, nfsConfig, heightMap):
        """
            Converts the true height map to a map of
            height accessible safely by the probe.
        """
        probeConfig = readConfigFile(nfsConfig['probeConfigFile']) 
        if probeConfig == None:
            raise Exception('Unable to read probe config file')
        dx = float(nfsConfig['trueXDimension']) / (nfsConfig['pointXDimension'] - 1)
        dy = float(nfsConfig['trueYDimension']) / (nfsConfig['pointYDimension'] - 1)
        ppX = math.ceil(float(probeConfig['dimensionX']) / dx)
        ppY = math.ceil(float(probeConfig['dimensionY']) / dx)
        #
        # TODO allow for second layer of probe dimensions
        #
        applicableHeighMap = []
        for i in range(0, nfsConfig['pointXDimension']):
            applicableHeightMap.append([])
            for j in range(0, nfsConfig['pointYDimension']):
                minX = max(i - ppX, 0)
                minY = max(j - ppY, 0)
                maxX = min(i + ppX, nfsConfig['pointXDimension']-1)
                maxY = min(j + ppY, nfsConfig['pointYDimension']-1)
                applicableHeightMap[i].append(_findMaxHeight(minX, minY, maxX, maxY, heightMap) + nfsConfig['measureDistance'])

        return applicableHeightMap

    def _findMaxHeight(self, minX, minY, maxX, maxY, heightMap):
        """Finds the maximum height in a given area of height map"""
        maxHeight = 0
        for i in range(minX, maxX+1):
            for j in range(minY, maxY+1):
                maxHeight = max(maxHeight, heightMap[i][j])
        return maxHeight
