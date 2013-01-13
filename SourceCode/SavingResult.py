from Queue import *
from threading import Thread
class SavingResult:

    
    
#konstruktor, predaje se put do direktorija u obliku npr."C:\Newfolder". znaci bez zadnjeg separatora
#broj koraka izmedu frekvencija, pocetna i zavrna frekvencija u Hz
#velicina plocice i pomak sonde u istoj velicini(cm,dm,m)
    def __init__(self, SavingResultConst):

        self.scanResultFolder=str (SavingResultConst['scanResultFolder'])
        self.freqSteps=int (SavingResultConst['freqSteps'])
        self.freqStart=float (SavingResultConst['freqStart'])
        self.freqStop=float (SavingResultConst['freqStop'])
        self.distanceFreq= float ((self.freqStop-self.freqStart)/(self.freqSteps))
        self.stepsPerScanX=int (SavingResultConst['stepsPerScanX'])
        self.stepsPerScanY=int (SavingResultConst['stepsPerScanY'])
        self.stepSize=float (SavingResultConst['stepSize'])
        
        self.tempX=0
        self.tempY=0
        self.oneLineResult=list()
        self.q=Queue()
        print "radim"
        self.t= Thread(target=self._saveOneLineResult)
        print "radim"
        self.t.daemon = True
        self.t.start()
        print "radim"

#metoda za privremenu pohranu podataka o jednoj toki. prima string result koji sadri
#popis amplituda od startFreq do stopFreq odvojenih zarezom
#rezultata mjerenja (amplituda) mora biti tocno self.steps+1
    def setPointResult(self,result):
        
        self.tempX+=self.stepsPerScanX*self.stepSize
        temp=result.split(',')
        self.oneLineResult.append(temp)
        
    def  saveOneLineResult(self):
        self.q.put(self.oneLineResult)
        self.oneLineResult=list()
        
    def waitCompletition(self):
        self.q.join()
        
#metoda se poziva na kraju redka i zapisuje rezultate o svim tockama u datoteke
# oblika x0y0,x1y0 itd u formatu freq,amplituda, u prvom retku pie i pozicija toke!
       
    def _saveOneLineResult(self):
        while (True):
            item=self.q.get()
            i=0
            for temp in item:
                j=0
                path=str(self.scanResultFolder)+"x_"+str(i*self.stepsPerScanX*self.stepSize)+"_y_"+str((self.tempY)*self.stepSize*self.stepsPerScanY)+".txt"
                
                foo=open(path,'w')
                foo.write("x_"+str(i*self.stepsPerScanX*self.stepSize)+"_y_"+str((self.tempY)*self.stepSize*self.stepsPerScanY)+"\n")
                for temp1 in temp:
                    foo.write(str(self.freqStart+j*self.distanceFreq)+','+str(temp1)+'\n')
                    j+=1
                i+=1
                foo.close()
            self.tempY+=self.stepsPerScanY*self.stepSize    
            self.tempX=0
            self.q.task_done()

