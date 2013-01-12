
import serial


class Motors:



    X=0

    Y=0

    Z=0

    
    # otvoriti ser.  komunikaciju s odgovarajucim parametrima
    def opensercom(self):#

        Motors.ser = serial.Serial(#
                        5,# COM6
                        baudrate = 9600,#
                        bytesize = 8,#
                        parity = 'N',#
                        stopbits = 1,#
                        timeout = 1,#
                        xonxoff = 0,#
                        rtscts = 0,#
                        dsrdtr = False)#
        
    # pomak po X osi ulijevo
    def moveXR(self,broj):  
        
        Motors.ser.write("1")#
        Motors.ser.write(chr(broj))#
        Motors.X=Motors.X+broj


    # pomak po X osi udesno
    def moveXL(self,broj): 

        Motors.ser.write("0")#
        Motors.ser.write(chr(broj))#
        Motors.X=Motors.X-broj

        
    # pomak po Y osi unatrag
    def moveYF(self,broj):
        
        Motors.ser.write("1")#
        Motors.ser.write(chr(broj))#
        Motors.Y=Motors.Y+broj


    # pomak po Y osi prema naprijed
    def moveYR(self,broj):  
        
        Motors.ser.write("0")#
        Motors.ser.write(chr(broj))#
        Motors.Y=Motors.Y-broj

        
    # pomak po Z osi dolje
#    def moveZD(self,broj):

#        Motors.ser.write("1")
#        Motors.ser.write(chr(broj))
#        Motors.Z=Motors.Z-broj
  
        
    # pomak po Z osi gore
#    def moveZU(self,broj):  
#
#        Motors.ser.write("0")
#        Motors.ser.write(chr(broj))
#        Motors.Z=Motors.Z+broj


    def reset(self):

        
        Sx=abs(Motors.X)
        Sy=abs(Motors.Y)
#        Sz=abs(Motors.Z)

        
        if Motors.X < 0:
            self.moveXR(Sx)
        else:
            self.moveXL(Sx)


        if Motors.Y < 0:
            self.moveYF(Sy)
        else:
            self.moveYR(Sy)


#       if Motors.Z < 0:
#            self.moveZU(Sz)
#        else:
#            self.moveZD(Sz)



        
        


    # zatvoriti port        
    def closesercom(self):#

        self.ser.close() #            
