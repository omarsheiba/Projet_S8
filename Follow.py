
"""
Follow the leader

"""


from Kilobot import *


def load(sim):
    return Follow(sim)

NEAR = 35
MID = 54
FAR = 69	

class Follow(Kilobot): 
    def __init__(self, sim):
        Kilobot.__init__(self, sim)

        self.id = self.secretID
        self.r = MID
        self.op = self.fullFWRD

        self.dist = 0
        self.timeout = 0

        self.time = 0

        self.last = 0
        self.x = 0

        self.var_stop = 0
        

        if (self.id == 0): # the leader
            self.set_color(0,3,0)
            self.program = [self.activate,
                            self.getX,
                            self.leader                       
                            ]

        else: # follower
            self.program = [self.activate,
                            self.getX,
                            self.follow,
                            ]


    ##
    ## Func
    ##
     
    def activate(self):
        self.message_out(self.id, 0, 0	)
        self.debug = str(self.id)
        self.toggle_tx()

        

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
        

    """def last_r(self):

        self.x += 1
        self.clear_rxbuf()
        self.get_message()
        print "Je recoit %d"%self.msgrx[1]
        if self.msgrx[1] > self.id:
            self.last = self.msgrx[1]
        else:
            self.last = self.id
        self.message_out(self.id , self.last , 0)
        self.toggle_tx()

        print "[%d]tmp_last = %d"%(self.id,self.last)
        if self.x <= 10:
            self.enable_tx()
            self.PC -= 1
        else:
            print "Mon last est %d"%self.last"""


    def leader(self):

        self.get_message()



        #Mouvement aleatoire tourner ou avancer
        
        if self.id == self.msgrx[0]-1 and self.dist <= self.r:
            self.x = 0
            move = self.rand()
            if move < 225:
                self.fullFWRD()     
            else:
                self.fullCCW()  #Changeable en self.fullCW()

        #On attend le suiveur        
        else:
            self.op = self.stop

        self.op()
        self.PC -= 2




    def send_stop(self):
        self.disable_tx()
        self.message_out( self.id , 0x01 , 0  )
        self.toggle_tx()



    def follow(self):
       

        if self.id == 2:
            print "[%d]le message vient de %d"%(self.id,self.msgrx[0])


        #Suiveur sortie de mon orbite
        if self.id == self.msgrx[0] - 1 and self.dist >= self.r and self.var_stop == 0:
            print"[%d] se stop parceque successeur plus la."%self.id
            if self.msgrx[0] == 2:
                self.set_color(3,1,2)
            self.var_stop += 1
            self.op=self.stop


        #Le suiveur est sorti de l'orbite du leader
        elif self.dist >= self.r and self.var_stop == 0 and self.id == self.msgrx[0] + 1:


            #On tourne a gauche pour suivre le leader
            if (self.time < 5 ):
                self.op = self.fullCCW
                self.time += 1
            #On tourne plus longtemps a droite et on avance pour se remettre dans l'axe
            elif (self.time >= 5 and self.time < 25):
                self.op = self.fullCW
                self.time += 1
            elif (self.time >= 25 and self.time <30):
                self.op = self.fullFWRD
                self.time += 1
            else:
                self.time = 0
                    

        #Le suiveur est dans l orbite et avance en meme temps que le leader
        elif self.dist < self.r and self.id == self.msgrx[0] + 1 and self.var_stop == 0:

            print "[%d] Est la"%self.id
            if self.id == 1:
                self.set_color(0,3,3)
            elif self.id == 2:
                self.set_color(3,0,3)
            elif self.id == 3:
                self.set_color(3,3,3)

            self.time = 0
            self.op = self.fullFWRD




            
        #Arret pour ne pas pousser un robot
        elif (self.id > self.msgrx[0] and self.dist <= 36) and self.var_stop == 0:
            print"[%d] se stop parceque trop pret"%self.id
            self.set_color(3,0,0)
            self.var_stop += 1
            self.op=self.stop

        #Robot inferieur en mode attente
        elif self.id < self.msgrx[0] and self.msgrx[1] == 1 and self.var_stop == 0:
            self.var_stop += 1
            self.op=self.stop
        
        #Robot en mode attente
        elif self.var_stop == 1:
            self.op=self.stop

            if self.id == self.msgrx[0] - 1 and self.dist < self.r:
                self.var_stop -= 1

        self.op()
        print "[%d] self var_stop = %d" %(self.id,self.var_stop)
        self.PC -= 2
