
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
        self.target = 0
        self.r = MID
        self.op = self.fullFWRD
        self.f_rdy = 0
        self.l_rdy = 0

        self.dist = 0
        self.timeout = 0

        self.time = 0

        self.last = 0
        self.x = 0

        self.var_stop = 0
        self.var_close = 0
        self.close_id = 0
        

        if (self.id == 0): # the leader
            self.set_color(0,3,0)
            self.program = [self.last_or_first,
                            self.activate,
                            self.initiate,

                            self.getX,
                            self.leader                       
                            ]

        else: # follower
            self.program = [self.last_or_first,
                            self.activate,
                            self.initiate,

                            self.getX,
                            self.follow,
                            ]


    ##
    ## Func
    ##
     

    def last_or_first(self):
        if self.id == 0:
            self.l_rdy = 1
        elif self.id == 2:
            self.f_rdy = 1

    def initiate(self):
        self.get_message()
        if self.msgrx[0] == self.id + 1 and self.f_rdy == 0:
            self.f_rdy = 1
        elif self.msgrx[0] == self.id - 1 and self.l_rdy == 0:
            self.l_rdy = 1
        elif self.l_rdy == 1 and self.f_rdy == 1:
            return

        print "[%d]lead = %d , follow = %d"%(self.id,self.l_rdy,self.f_rdy)
        self.PC -= 1


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

        if self.id == 1 and self.msgrx[0] == 0:
            print "[%d] / [%d] = %d"%(self.id,self.msgrx[0],self.dist)

        self.PC -= 1       
        


    def leader(self):

        #Mouvement aleatoire tourner ou avancer
        if self.id == self.msgrx[0] - 1 and self.dist <= self.r-2:
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
   



        #Suiveur sortie de mon orbite
        if self.id == self.msgrx[0] - 1 and self.dist >= self.r and self.var_stop == 0 and self.var_close == 0:
            print"[%d] se stop parceque successeur plus la."%self.id
            if self.msgrx[0] == 2:
                self.set_color(2,1,2)
            self.var_stop += 1
            self.op=self.stop


        #Le suiveur est sorti de l'orbite du leader
        elif self.dist >= self.r and self.var_stop == 0 and self.var_close == 0:

            if (self.time < 17 ):
                self.op = self.fullCCW
                self.time += 1
            #On tourne plus longtemps a droite et on avance pour se remettre dans l'axe
            elif (self.time >= 17 and self.time < (15 + self.x)):
                self.op = self.fullFWRD
                self.time += 1
            else:
           
                self.time = 0
                self.x += 7
                    

        #Le suiveur est dans l orbite et avance en meme temps que le leader
        elif self.dist < self.r and self.id == self.msgrx[0] + 1 and self.var_stop == 0 and self.var_close == 0:

            if self.id == 1:
                self.set_color(0,3,3)
            elif self.id == 2:
                self.set_color(3,2,1)
            elif self.id == 3:
                self.set_color(3,3,3)

            self.x = 0
            self.time = 0
            self.op = self.fullFWRD


        #Arret pour ne pas pousser un robot
        elif (self.id > self.msgrx[0] and self.dist <= 34) and self.var_stop == 0 and self.var_close == 0:
            print"[%d] se stop parceque trop pret"%self.id
            self.set_color(3,0,0)
            self.var_close += 1
            self.close_id = self.msgrx[0]
            self.op=self.stop

        
        #Robot inferieur en mode attente
        elif self.id < self.msgrx[0] and self.msgrx[1] == 1 and self.var_stop == 0 and self.var_close == 0:
            self.var_stop += 1
            self.op=self.stop
        
        #Robot en mode attente
        elif self.var_stop == 1:
            self.op=self.stop
            self.send_stop()

            if (self.id == self.msgrx[0] - 1 and self.dist < self.r):
                self.var_stop -= 1


        elif self.var_close == 1:
            self.op=self.fullCCW

            if self.dist >= 36 and self.msgrx[0] == self.close_id:
                self.var_close -= 1

        self.op()
        self.PC -= 2

