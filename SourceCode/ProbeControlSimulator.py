
import random
from UserString import MutableString

class ProbeControl:

    def __init__(self, nfsConf):
        self.freqSteps = int(nfsConf['freqSteps'])

    def scan(self):
        result = MutableString()
        for i in range(self.freqSteps+1):
            result += str(random.random())
            if i != self.freqSteps:
                result += ","
        return result
