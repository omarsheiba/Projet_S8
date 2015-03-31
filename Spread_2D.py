from Kilobot import *
from math import *

def load(sim):
    return Spread_1D(sim)

NEAR = 35
MID = 54
FAR = 69

class Spread_1D(Kilobot): 
    def __init__(self, sim):
        Kilobot.__init__(self, sim)
        
        
        self.id = self.secretID
        self.r = MID
        self.op = self.fullFWRD
        self.x=0
        self.dist = 0
        self.timeout = 0

        self.program=[self.moveL,
        self.printa]

    ##
    ## Func
    ##
     
    def printa(self):
        print("my id is",self.id,"and my position is",self.pos)
    def activate(self):
        self.message_out(self.id, 0, 0)
        self.debug = str(self.id)
        self.toggle_tx()

    def demitour(self):
        self.orientation =0
    


        
    def moveL(self): 
        if self.id !=0 and floor(self.pos[0])<floor(self.id*(750)/(self.sim.config['n'])):
            self.demitour()
            self.set_motor(64,64)
            self.PC-=1
        if self.id != 0 and floor(self.pos[0])>self.id*(750)/(self.sim.config['n']):
            if self.orientation ==180:
                self.set_motor(64,64)
                print("trop tard",self.pos)
                self.PC-=1
        if (floor(self.pos[0])==self.id*(750)/(self.sim.config['n']) or self.pos[0]==16):
            if (floor(self.pos[1])==150 or floor(self.pos[1])==450):
                self.stop()
                return
            for i in range (0,self.sim.config['n']):
                if self.id==i:
                    if i ==0: 
                        self.quartdetour()
                        self.fullFWRD
                        print(self.pos)
                    if i % 2 ==0 and i>0:
                        self.quartdetour()                   
                        while(self.pos[1]>100):
                            self.set_motor(64,64)
                            print(self.pos)
                    else:
                        self.troisquartdetour()
                        self.set_motor(64,64)
            self.PC-=1

        else:   
            self.stop()        
            return