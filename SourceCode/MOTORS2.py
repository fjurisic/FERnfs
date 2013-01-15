
import serial


class Motors:


    X=0

    Y=0

    Z=0

    
    # otvoriti ser.  komunikaciju s odgovarajucim parametrima
    def opensercom(self):

        Motors.ser = serial.Serial(
                        5,# COM6
                        baudrate = 9600,
                        bytesize = 8,
                        parity = 'N',
                        stopbits = 1,
                        timeout = 1,
                        xonxoff = 0,
                        rtscts = 0,
                        dsrdtr = False)
        
        
    # pomak po X osi udesno
    def moveXR(self,broj):  
        
        Motors.ser.write("1")
        Motors.ser.write(chr(broj))
        Motors.X=Motors.X+broj


    # pomak po X osi ulijevo
    def moveXL(self,broj): 

        Motors.ser.write("0")
        Motors.ser.write(chr(broj))
        Motors.X=Motors.X-broj

        
    # pomak po Y osi prema naprijed
    def moveYF(self,broj):
        
        Motors.ser.write("1")
        Motors.ser.write(chr(broj))
        Motors.Y=Motors.Y+broj


    # pomak po Y osi unatrag
    def moveYR(self,broj):  
        
        Motors.ser.write("0")
        Motors.ser.write(chr(broj))
        Motors.Y=Motors.Y-broj

        
    # pomak po Z osi gore
    def moveZU(self,broj):  

        Motors.ser.write("1")
        Motors.ser.write(chr(broj))
        Motors.Z=Motors.Z+broj


    # pomak po Z osi dolje
    def moveZD(self,broj):

        Motors.ser.write("0")
        Motors.ser.write(chr(broj))
        Motors.Z=Motors.Z-broj
  
    # reset
    def reset(self):
        
        Sx=abs(Motors.X)
        Sy=abs(Motors.Y)
        Sz=abs(Motors.Z)

        
        if Motors.Z < 0:
            self.move(0,0,Sz)
        else:
            self.move(0,0,-Sz)
        
        if Motors.X < 0:
            if Motors.Y < 0:
                self.move(Sx,Sy,0)
            else:
                self.move(Sx,-Sy,0)
        else:
            if Motors.Y < 0:
                self.move(-Sx,Sy,0)
            else:
                self.move(-Sx,-Sy,0)


    # glavna metoda za upravljanje motorima
    def move(self, b1, b2, b3):

        Bx=abs(b1)
        By=abs(b2)
        Bz=abs(b3)

        
        if Bx>255:
            d1=Bx/255
            m1=Bx%255
            while(d1>0):
                if b1 < 0:
                    self.moveXL(255)
                else:
                    self.moveXR(255)
                self.moveYF(0)
                self.moveZU(0)
                d1=d1-1
            if b1 < 0:
                self.moveXL(m1)
            else:
                self.moveXR(m1)
        else:
            if b1 < 0:
                self.moveXL(Bx)
            else:
                self.moveXR(Bx)
            

        if By>255:
            d2=By/255
            m2=By%255
            if b2 < 0:
                self.moveYR(m2)
            else:
                self.moveYF(m2)
            if d2>0:
                self.moveZU(0)
                while(d2>0):
                    self.moveXR(0)
                    if b2 < 0:
                        self.moveYR(255)
                    else:
                        self.moveYF(255)
                    if d2==1:
                        break
                    else:
                        self.moveZU(0)
                    d2=d2-1
        else:
            if b2 < 0:
                self.moveYR(By)
            else:
                self.moveYF(By)


        if Bz>255:
            d3=Bz/255
            m3=Bz%255
            if b3 < 0:
                self.moveZD(m3)
            else:
                self.moveZU(m3)
            while(d3>0):
                self.moveXR(0)
                self.moveYF(0)
                if b3 < 0:
                    self.moveZD(255)
                else:
                    self.moveZU(255)
                d3=d3-1
        else:
            if b3 < 0:
                self.moveZD(Bz)
            else:
                self.moveZU(Bz)

                   
    # zatvoriti ser.  komunikaciju       
    def closesercom(self):

        self.ser.close()             
