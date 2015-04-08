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
        if self.id!=self.sim.config['n']-1:
            self.program=[self.moveL,
            self.printa,
            self.cover,
            self.uncover,
            self.loop2,
            self.hamid,
            self.hamid]
        else:
            self.program=[self.activateL,
            self.loop1]

    ##
    ## Func
    ##
    def hamid (self):
        print("my name is hamid",self.id,"and the tresure is in",self.msgrx[0],self.msgrx[1])
        self.set_color(0,3,0)
        self.PC-=1
    def printa(self):
        if self.id==5:
            self.wait()
            self.wait()
            self.wait()
            self.wait()
            self.wait()
            self.wait()
            self._delay_ms(1000)
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
        self.message_out(self.pos[0],self.pos[1],0)
        self.debug = str(self.id)
        self.toggle_tx()

    def demitour(self):
        self.orientation =0
    

    def cover(self):
            self.get_message()
            if self.msgrx[0]>10 :
                self.message_out(self.msgrx[0],self.msgrx[1],0)
                self.stop()
                self.PC+=4
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
            self.clear_rxbuf()      
            return
        #if floor(self.pos[0])>self.id*(750)/(self.sim.config['n']):
         #   self.message_out(self.id,self.id,self.id)

    def quartdetour(self):
        self.orientation =270
    def troisquartdetour(self):
        self.orientation = 90

                
