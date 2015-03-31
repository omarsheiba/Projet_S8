from Kilobot import *

def load(sim):
    return untitled(sim)

class untitled(Kilobot): 
    def __init__(self, sim):
        Kilobot.__init__(self, sim)

        self.secretID = len (sim.bots)
        self.id = self.secretID
        
        self.op = self.fullFWRD

        self.gradient_value = 0 
        self.var_distance = 0

        if  self.id<6: # the leader
            self.set_color(0,3,0)
            self.program = [self.activate, 
                        self.loop]
        else: # others
            self.set_color(0,0,3)
            self.program = [self.printa]                                


    def activate(self):   
        for i in range(0,6):
            if self.id==i:
                self.gradient_value = i
        self.message_out (self.id,self.gradient_value,0)
        self.debug = str(self.id)
        self.toggle_tx()


    def wander(self):
        move = self.rand()
        if move < 225:
            self.fullFWRD()
        else:
            self.fullCCW()

    def printa(self):
        self.get_message()
        if(self.msgrx[5]!=1):
            self.wander()
            self.get_message()
            self.PC -=1 
        if(self.msgrx[5]==1):
            self.gradient_value=(self.msgrx[2] + 1)
            print(self.gradient_value)
            
            self.PC-=1
