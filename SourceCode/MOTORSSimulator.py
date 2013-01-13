class Motors:
    X = 0
    Y = 0
    Z = 0

    def move(self, moveX, moveY, moveZ):
        self.opensercom()
        if moveX >= 0:
            self.moveXR(moveX)
        else:
            self.moveXL(-1*moveX)
        if moveY >= 0:
            self.moveYF(moveY)
        else:
            self.moveYR(moveY)
        # moveZ
        self.closesercom()

    def opensercom(self):
        print "M: Opening serial communication"

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
        Sx = abs(self.X)
        Sy = abs(self.Y)
        print "M: Reseting"
        if self.X < 0:
            self.moveXR(Sx)
        else:
            self.moveXL(Sx)

        if self.Y < 0:
            self.moveYF(Sy)
        else:
            self.moveYR(Sy)

    def closesercom(self):
        print "M: Closing serial communication"
