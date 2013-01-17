import time

class Motors:
    X = 0
    Y = 0
    Z = 0

    def opensercom(self):
        print "M: Opening serial communication"

    def sendconst(self, const):
        print "M: Sending step constant "+str(const)

    def startpoint(self):
        print "M: Declaring start point"

    def moveXR(self, broj):
        print "M: X+ "+str(broj)
        self.X = self.X + broj
        
    def moveXL(self, broj):
        print "M: X- "+str(broj)
        self.X = self.X - broj

    def moveYF(self, broj):
        print "M: Y+ "+str(broj)
        self.Y = self.Y + broj

    def moveYR(self, broj):
        print "M: Y- "+str(broj)
        self.Y = self.Y - broj

    def reset(self):
        print "M: Reseting"

    def move(self, x, y, z):
        print "M: X|"+str(x)+" Y|"+str(y)+" Z|"+str(z)
        time.sleep(0.25*(abs(x)+abs(y)+abs(z)))

    def closesercom(self):
        print "M: Closing serial communication"
