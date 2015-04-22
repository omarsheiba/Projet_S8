### Simulation ## ./launch -n 8 -p Bots/spirale2.py -f CIRCLE2

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
			    #self.toggle_tx,
			    self.hearbarrier,
			    #self.toggle_g,
			    self.loop2
                            ]
	elif (self.id == 1): # the leader, the first violin
	    self.set_color(3,3,0)
            self.program = [self.setmsg,
			    #self.activate,
			    self.toggle_tx,
			    self.hearbarrier,
			    #self.toggle_g,
			    self.loop2
                            ]


	
	


        else:
            self.set_color(3,3,3)
            self.program = [self.setmsg,
                            self.initial,
                            #self.toggle_tx,
                            self.getX,
                            #self.CCW,
			    self.FWRD,
			    #self.APS,
                            self.doSpiral,
                            self.hearbarrier,                           			    
			    self.timer,
                            self.toggle_r,
                            self.loop2
                            ]



    ##
    ## Func
    ##



    def setmsg(self):
        self.message_out(0x10,0x20,0x30) # note that the last one gets masked to 0xFE




    def timer(self):
	print"azazaz"
        if self.timee > 1200:
            self.PC -= 2
            self.timee +=1 
        

    def activate(self):
        self.message_out(self.id, 0, 0	)
        self.debug = str(self.id)
        self.toggle_tx()
        print "%d active son aura"%self.id



    def initial(self):
        self.timee= 0
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
        


    def FWRD(self):

        
        if(self.timeFWRD < 40):
            self.x = 0
            move = self.rand()
            
            self.midFWRD()  
	   
            self.timeFWRD += 1
            self.op()
        
            self.PC -= 2






    def doSpiral(self): # spiral towards the swarm; turn, forward or finish
        self.timee +=1 
	#print(self.timee)
	if self.timee > 1000:
            self.PC += 3
	
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




    def hearbarrier(self):
	
        data = distance = 0
        self.get_message()
	#if(self.id == 2):
        if (self.msgrx[5] == 1):
	    print("Le robot %d a trouve un tresor apres %d "%(self.id,self.timee))
            self.var_data = [self.msgrx[0], self.msgrx[1], self.msgrx[2]]
            self.var_distance = self.msgrx[3]

        else:
            self.PC -= 3
	#else:
	    #self.PC -=2
