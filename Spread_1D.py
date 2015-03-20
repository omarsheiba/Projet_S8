from Kilobot import *

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
            self.program = [self.getX,
                            self.activate,
                            self.loop2,                         
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


    def getX(self):
        self.wait()
        print("en attente")
        self.get_message()
        if (self.msgrx[5] != 1):
            print("le message na pas ete get")
            self.op=self.fullFWRD
            #if (self.msgrx[3] < self.r):
            self.op()
            self.PC -= 1 
        else:
            if(self.msgrx[3]<69):
                self.dist = self.msgrx[3]
                print(self.dist)
                print("il faut faire demitour")
                self.clear_rxbuf()
                self.demitour(5)
                if self.msgrx[3]<=69:
                    self.midFWRD()               
                
            
