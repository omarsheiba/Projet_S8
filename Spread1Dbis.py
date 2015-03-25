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

        if (self.id == 0): # the leader
            self.set_color(0,3,0)
            self.program = [self.activate,
                            self.loop,                         
                            ]

       
        else: # others
            self.set_color(0,0,3)
            self.program = [self.moveL,
                            self.loop1,                         
                            ]

    ##
    ## Func
    ##
     
    def activate(self):
        self.message_out(self.id, 0, 0)
        self.debug = str(self.id)
        self.toggle_tx()

    def demitour(self, speed):
        self.speed = speed
        degrees = self.speed
        self.orientation =0

    """def turn(self):
        self.turnLFoot(5)
        self.x += 1
        if (self.x < 10):
            self.PC -= 1 """

    """def go(self):
        self.fullFWRD()
        self.x -= 1
        if (self.x > 0):
            self.PC -= 1 """
    """def getX(self):
        print("en attente")
        self.get_message()
        for v in range(1,5):
            if (v==self.id):
                print("my id is",self.id)
                if(self.msgrx[5] != 1):
                    print("le message na pas ete get")
                    self.fullFWRD()
                    self.PC-=1
                else:            
                    self.activate() 
                                 
            else:  
                print("delai")
                self._delay_ms(3000)

        def react(self):
        self.get_message()
        if(self.msgrx[5]==1)"""

        
    def moveL(self): 
        if(floor(self.pos[0])!=(self.id)*70):
            self.set_motor(64,64)
            
        else:
            print("my id is""and my position is",self.id,self.pos)
