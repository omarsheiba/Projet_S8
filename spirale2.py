### Simulation ## ./launch -n 8 -p Bots/spirale3.py -f CIRCLE2 

from Kilobot import *


def load(sim):
    return Test(sim)

NEAR = 35
MID = 54
FAR = 69 
DONE = 0xC
TURN = 19

class Test(Kilobot): 
    def __init__(self, sim):
        Kilobot.__init__(self, sim)

        self.id = self.secretID
        self.r = MID
        self.op = self.fullFWRD

        self.dist = 0
        self.timeout = 0
        self.time = 0
	self.timeFWRD = 0
        self.count = 0
        self.last = 0
        self.time1 = 30
	self.timeFWRD1 = 30
        self.spiral = 0 # spiral
        self.scount = 0

        self.top = 0

	if (self.id == 0): # the leader, the first violin
	    self.set_color(3,3,0)
            self.program = [self.setmsg,
			    #self.activate,
			    self.toggle_tx,
			    self.hearbarrier,
			    #self.toggle_g,
			    self.loop
                            ]



        else:
            self.set_color(3,3,3)
            self.program = [self.setmsg,
                            self.toggle_tx,
                            self.getX,
                            #self.CCW,
			    self.FWRD,
			    #self.APS,
			    #self.initial,
			    self.doSpiral,
			    #self.hearbarrier,
                            #self.toggle_g,
                            self.loop2
                            ]


    ##
    ## Func
    ##
     
   

    def setmsg(self):
        self.message_out(0x10,0x20,0x30) # note that the last one gets masked to 0xFE


    def activateL(self):
        self.id = 0
        print "0 assumes position as 0"
        self.debug = "S:0"
        self.message_out(0,0,GO)
        self.toggle_tx()
        self.set_color(0,3,0)
        return self.goto(self.hold)

    

    def activate(self):
        self.message_out(self.id, 0, 0	)
        self.debug = str(self.id)
        self.toggle_tx()
        print "%d active son aura"%self.id



    def hearbarrier(self):
	print"hear"
        data = distance = 0
        self.get_message()
        if (self.msgrx[5] == 1):
            self.var_data = [self.msgrx[0], self.msgrx[1], self.msgrx[2]]
            self.var_distance = self.msgrx[3]
        else:
            self.PC -= 2


    def initial(self):
	self.spiral = 0
	self.count = 0
	self.scount = 0
	self.timeFWRD = 0
	self.time = 0
	self.time1 = 0
	self.timeFWRD1 = 0
 	print "initialisation"



    def getX(self):

        self.get_message()
        if (self.msgrx[5] == 1):
            if (self.msgrx[3] < self.r):
                self.dist = self.msgrx[3]
                return
            
        self.timeout += 1
        if (self.timeout > 3):
            self.timeout = 0
            self.dist = FAR

            return
        self.PC -= 1       
        
    def CCW(self):


        if(self.time < 20):
            self.x = 0
            move = self.rand()
            
            self.fullCCW()  #Changeable en self.fullCW()
	    print "CCW"
            self.time += 1
            self.op()
        
            self.PC -= 2

    def FWRD(self):

        
        if(self.timeFWRD < 20):
            self.x = 0
            move = self.rand()
            
            self.midFWRD()  
	    print "FWD"
            self.timeFWRD += 1
            self.op()
        
            self.PC -= 2

    def APS(self):
	print"A"

        if(self.time1< 20):
	    print"C"
            self.x = 0
            move = self.rand()
            
            self.fullCCW()  #Changeable en self.fullCW()

            self.time1 += 1
            self.op()
        
            self.PC -= 2


        
        elif(self.timeFWRD1 < 20):
	    print"F"
            self.x = 0
            move = self.rand()
            
            self.midFWRD()  #Changeable en self.fullCW()

            self.timeFWRD1 += 1
            self.op()
        
            self.PC -= 2

    def doSpiral(self): # spiral towards the swarm; turn, forward or finish
	print"spiral"
        self.scount += 1
	self.toggle_g
        if (self.scount < TURN):
            self.fullCCW()
	    #print "CCW"
	    #self.loop2
	    self.count += 1
        elif (self.scount <= TURN + self.spiral):
            self.midFWRD()
	    #print "FWRD"
	    #self.loop2
	    self.count += 1
	#elif (self.count > 270):     # 100, 270, 450
	 #   self.PC -=3
        else:
            #self.hold
	    #print "maintenant"
	    self.scount = 0
            self.spiral += 3

    def setmsg(self):
        self.message_out(0x10,0x20,0x30) # note that the last one gets masked to 0xFE


    def hearbarrier(self):
	print"hearrr"
        data = distance = 0
        self.get_message()
	#if(self.id == 2):
        if (self.msgrx[5] == 1):
            self.var_data = [self.msgrx[0], self.msgrx[1], self.msgrx[2]]
            self.var_distance = self.msgrx[3]
        else:
            self.PC -= 2
	#else:
	    #self.PC -=2

    def hold(self):
        self.PC -= 1
        self.get_message()
        if (self.msgrx[5] == 1):

            heard = self.msgrx[0]
            top   = self.msgrx[1]
            mode  = self.msgrx[2]
            dist  = self.msgrx[3]

            if (top > self.top): # to help others, all of the swarm shouts the top
                self.top = top
                self.message_out(self.id, self.top, mode)

            if (mode == DONE): # finish trigger
                self.enable_tx()
                self.message_out(self.id, self.top, DONE)
                self.set_color(0,3,0)

            self.reset_rx()
