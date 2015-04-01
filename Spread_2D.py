from Kilobot import *
from math import *

def load(sim):
    return Spread_1D(sim)

NEAR = 58
MID = 89
FAR = 90

class Spread_1D(Kilobot): 
    def __init__(self, sim):
        Kilobot.__init__(self, sim)
        
        
        self.id = self.secretID
        self.r = MID
        self.op = self.fullFWRD
        self.x=0
        self.dist = 0
        self.timeout = 0
        # if self.id!=self.sim.config['n']-1:
        self.program=[self.moveL,
        self.printa,
        self.cover,
        self.uncover,
        self.loop2,
        self.printa]
        # else:
        #     self.program=[self.activate,
        #     self.loop1]

    ##
    ## Func
    ##
     
    def printa(self):
        if self.id==5:
            self._delay_ms(2000)
            self.activate()
            return
        #print("my id is",self.id,"and my position is",self.pos)
        if self.msgrx[5]==1 and self.id!=5:
            self.activate()
            self.wait()
            return
        else:
            self.get_message()
            self.PC-=1

    def activate(self):
        self.message_out(self.id, 0, 0)
        self.debug = str(self.id)
        self.toggle_tx()
    def activateL(self):
        self.message_out(self.pos[0], 0, 0)
        self.debug = str(self.id)
        self.toggle_tx()
        print(self.msgrx[0])

    def demitour(self):
        self.orientation =0
    

    def cover(self):
            if self.msgrx[0]>10 or self.x==1 :
                self.rx_buff=self.msgrx[0]
                print(self.rx_buff)
                self.get_message(rx_buff,0,0)
                self.x=1
                self.troisquartdetour()
                if self.id !=0 and floor(self.pos[0])!=floor(self.id*(750)/(self.sim.config['n'])):
                    self.set_motor(64,64)
                    self.PC-=1
                elif self.id==0 and floor(self.pos[0])!=16:
                    self.set_motor(64,64)
                    self.PC-=1
                else: 
                    return
            if (floor(self.pos[1])==100):
                self.stop()
                return
            for i in range (0,self.sim.config['n']):
                if self.id==i:
                    if i ==0: 
                        self.quartdetour()
                        self.set_motor(64,64)
                    else:#if i % 2 ==0 and i>0:
                        self.quartdetour()                   
                        self.set_motor(64,64)
                    #else:
                     #   self.troisquartdetour()
                      #  self.set_motor(64,64)
            self.PC-=1

    def uncover(self):
        if (floor(self.pos[1])==450):
            self.stop()
            return
        for i in range (0,self.sim.config['n']):
                if self.id==i:
                    if i ==0: 
                        self.troisquartdetour()
                        self.set_motor(64,64)
                    else:#if i % 2 ==0 and i>0:
                        self.troisquartdetour()                   
                        self.set_motor(64,64)
                    #else:
                     #   self.troisquartdetour()
                      #  self.set_motor(64,64)
        self.PC-=1

        
    def moveL(self): 
        if self.id !=0 and floor(self.pos[0])<floor(self.id*(750)/(self.sim.config['n'])):
            self.demitour()
            self.set_motor(64,64)
            self.PC-=1
        if self.id != 0 and floor(self.pos[0])>self.id*(750)/(self.sim.config['n']):
            if self.orientation ==180:
                self.set_motor(64,64)
                self.PC-=1
        else:   
            self.stop()        
            return
        #if floor(self.pos[0])>self.id*(750)/(self.sim.config['n']):
         #   self.message_out(self.id,self.id,self.id)

    def quartdetour(self):
        self.orientation =270
    def troisquartdetour(self):
        self.orientation = 90
