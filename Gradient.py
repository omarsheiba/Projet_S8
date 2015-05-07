from Kilobot import *

def load(sim):
    return untitled(sim)

class untitled(Kilobot): 
    def __init__(self, sim):
        Kilobot.__init__(self, sim)

        self.r = 58
        self.r1 = 40

        
        self.secretID = len (sim.bots)
        self.id = self.secretID
        self.dist = 0
        self.timeout = 0
        self.timeout1 =0
        self.timeout2=0
        self.time = 0

        self.op = self.fullFWRD

        self.gradient_walker = 0
        self.var_distance = 0

        if  self.id<6: # beacon
            self.set_color(0,3,0)
            self.program = [self.activate, 
                        self.loop]
        else: # walker
            self.set_color(0,0,3)
            self.program = [self.getX,
                            self.react,
                            self.getX2,
                            self.react2
                            ]


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
        #print (self.msgrx[5])
        if(self.msgrx[5]!=1):
            self.wander()
            self.get_message()
            self.PC -=1 
        if(self.msgrx[5]==1):
            print ("NTR")
            self.gradient_walker=(self.msgrx[1])
        
    def  moveforward(self):

        timeout +=1
        if (timeout1 < 5):
            timeout +=1
            self.fullFWRD()

    def demitour(self):
        self.orientation=0

    def getX(self):

        self.get_message()
        #print (self.msgrx[5])
        if (self.msgrx[5] == 1 and self.msgrx[1] == self.gradient_walker):
            #print ("OKAY")
            #(self.msgrx[2] == self.gradient_value + 1):
               # self.gradient_value= self.msgrx[2]
                #print("gradient")
            if (self.msgrx[3] < self.r and self.msgrx[3] > self.r1):
                #print("oui")
                self.dist = self.msgrx[3]
                #print(self.dist)
                return

            elif (self.msgrx[3]<self.r1):
                self.dist = self.msgrx[3]
                return 
                 
            #elif (self.gradient_value < self.msgrx[2]):
             #   print("OK ?")

              #  if (self.time <17):
                    #self.op =self.fullCCW 
                    #self.time +=1
                    #return
                    #self.PC =-2

        self.timeout+=1
        if(self.timeout>3):
            #print("non")
            self.timeout = 0
            self.dist= 73
            return 
        self.PC=-1


        #self.timeout += 1
        #print (self.timeout)
        #if (self.timeout > 3):
            #self.timeout = 0
            #self.dist = 69
            #print("merde")
            #return
            #self.PC -= 1     


        
    def react(self):
        
        if (self.gradient_walker==self.msgrx[1]):
            self.fullFWRD

            #if (self.dist > self.r and self.gradient_walker%2==0):
                #self.op = self.fullCCW
                
            if (self.dist > self.r): 
                #and self.gradient_walker%2==1):
                self.op = self.fullCCW

            elif (self.dist < self.r1):

                self.orientation=0
                timeout1=+1

                if (timeout1<2):
                    self.fullFWRD()
                    self.PC=-1

            elif(self.dist < self.r and self.dist > self.r1):
                self.op = self.fullFWRD 
                

        elif (self.gradient_walker +1 == self.msgrx[1]):    
            self.gradient_walker=self.msgrx[1]

        elif (self.gradient_walker==5):
            return 

        print (self.gradient_walker)
        print (self.dist)
        self.op()
        self.PC -= 2


def getX2(self): 

        #print (self.msgrx[5])
        if (self.msgrx[5] == 1):
            #print ("OKAY")
            #(self.msgrx[2] == self.gradient_value + 1):
               # self.gradient_value= self.msgrx[2]
                #print("gradient")
            if (self.msgrx[3] < self.r and self.msgrx[3] > self.r1):
                #print("oui")
                self.dist = self.msgrx[3]
                #print(self.dist)
                return

            elif (self.msgrx[3]<self.r1):
                self.dist = self.msgrx[3]
                return 
                 
            #elif (self.gradient_value < self.msgrx[2]):
             #   print("OK ?")

              #  if (self.time <17):
                    #self.op =self.fullCCW 
                    #self.time +=1
                    #return
                    #self.PC =-2

        self.time+=1
        if(self.time>3):
            #print("non")
            self.time = 0
            self.dist= 73
            return 
        self.PC=-1


        #self.timeout += 1
        #print (self.timeout)
        #if (self.timeout > 3):
            #self.timeout = 0
            #self.dist = 69
            #print("merde")
            #return
            #self.PC -= 1

    def react2(self): 

        if (self.gradient_walker==self.msgrx[1]):
            self.fullFWRD

            #if (self.dist > self.r and self.gradient_walker%2==0):
                #self.op = self.fullCCW
                
            if (self.dist > self.r): 
                #and self.gradient_walker%2==1):
                self.op = self.fullCCW

            elif (self.dist < self.r1):

                self.orientation=180
                print("Yeah")
                timeout2=+1

                if (timeout2<2):
                    timeout2+=1
                    self.fullFWRD()
                    self.PC=-1

            elif(self.dist < self.r and self.dist > self.r1):
                self.op = self.fullFWRD 
                

        elif (self.gradient_walker - 1 == self.msgrx[1]):    
            self.gradient_walker=self.msgrx[1]

        print (self.gradient_walker)
        print (self.dist)
        self.op()
        self.PC -= 2
