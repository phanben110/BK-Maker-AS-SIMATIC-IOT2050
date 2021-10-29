import numpy as np  
import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np  
from linearRegession.neuralNetwork.BEN_model import linearRegression 
import torch 
from torch.autograd import Variable

class TuningPID():
    def __init__ (self,pathKp="models/kp.pt", pathKi="models/ki.pt", pathKd="models/kd.pt", useCuda=True, debug=True): 

        """                                        
        kp, ki, kd : is value of PID 
        k1, k2, k3 : is the value after evaluation 
            k1 : Settling time 
            k2 : Overshoot 
            k3 : Steady State Error 
        q1, q2, q3, q4 : is the mode slection
            q1 : Settling time 
            q2 : Overshoot  
            q3 : Steady State Error  
            q4 : Stability 
        """

        self.kp = None 
        self.ki = None 
        self.kd = None 

        self.k1 = None
        self.k2 = None
        self.k3 = None 

        self.q1 =False 
        self.q2 =False  
        self.q3 =False 
        self.q4 =False  

        self.pathKp = pathKp 
        self.pathKi = pathKi
        self.pathKd = pathKd 
        self.useCuda = useCuda 
        self.debug = debug
        
        self.xTestKp = None#np.array([self.ki,self.kd,self.k1,self.k2,self.k3],dtype=np.float32).T   
        self.xTestKi = None#np.array([self.kp,self.kd,self.k1,self.k2,self.k3],dtype=np.float32).T    
        self.xTestKd = None#np.array([self.kp,self.ki,self.k1,self.k2,self.k3],dtype=np.float32).T    
        
        self.modelKp = None 
        self.modelKi = None 
        self.modelKd = None 
    
    def loadModel(self,pathModel):

        if self.useCuda: 
            if torch.cuda.is_available(): 
                device = torch.device("cuda")
                model = linearRegression(5,1)
                model.load_state_dict(torch.load(pathModel,map_location="cuda:0"),strict=False)
                model.to(device)
                if self.debug: 
                    print(f"init model {pathModel} with cuda")
            else: 
                modelKp = linearRegression(5, 1)
                modelKp.load_state_dict(torch.load(pathModel), strict=False)
                if self.debug: 
                    print(f"init model {pathModel} with CPU")
        else: 
            modelKp = linearRegression(5, 1)
            modelKp.load_state_dict(torch.load(pathModel), strict=False)
            if self.debug: 
                print(f"init model {pathModel} with CPU")

        model.eval()
        return model

    def predicted(self,model,xTest):
        with torch.no_grad(): 
            if self.useCuda: 
                if torch.cuda.is_available(): 
                    output = model(Variable(torch.from_numpy(xTest).cuda())).cpu().data.numpy()
                else: 
                    output = model(Variable(torch.from_numpy(xTest))).data.numpy()
            else: 
                output = model(Variable(torch.from_numpy(xTest))).data.numpy()
        return output 

    def loadPIDmodel(self): 
        self.modelKp = self.loadModel(self.pathKp)
        self.modelKi = self.loadModel(self.pathKi) 
        self.modelKd = self.loadModel(self.pathKd) 

    def preProcessData(self): 
        self.xTestKp = np.array([self.ki,self.kd,self.k1,self.k2,self.k3],dtype=np.float32).T   
        self.xTestKi = np.array([self.kp,self.kd,self.k1,self.k2,self.k3],dtype=np.float32).T    
        self.xTestKd = np.array([self.kp,self.ki,self.k1,self.k2,self.k3],dtype=np.float32).T    

    def tuningPID(self):
        self.preProcessData()
        kp = self.predicted(self.modelKp, self.xTestKp )
        self.kp=kp[0]
        self.preProcessData()
        ki = self.predicted(self.modelKi, self.xTestKi) 
        self.ki=ki[0]
        self.preProcessData()
        kd = self.predicted(self.modelKd, self.xTestKd)
        self.kd=kd[0]

    def tuningIPD(self): 
        self.preProcessData()
        ki = self.predicted(self.modelKi, self.xTestKi )
        self.ki=ki[0]

        self.preProcessData()
        kp = self.predicted(self.modelKp, self.xTestKp) 
        self.kp=kp[0]

        self.preProcessData()
        kd = self.predicted(self.modelKd, self.xTestKd)
        self.kd=kd[0]

    def tuningDPI(self): 
        self.preProcessData()
        kd = self.predicted(self.modelKd, self.xTestKd )
        self.kd=kd[0]

        self.preProcessData()
        kp = self.predicted(self.modelKp, self.xTestKp) 
        self.kp=kp[0]

        self.preProcessData()
        ki = self.predicted(self.modelKi, self.xTestKi)
        self.ki=ki[0]


    def beginTuning(self,kp=None,ki=None,kd=None,k1=None,k2=None,k3=None,q1=False,q2=False,q3=False,q4=False): 
        self.kp=kp 
        self.ki=ki
        self.kd=kd

        self.k1=k1
        self.k2=k2
        self.k3=k3 

        self.q1=q1
        self.q2=q2
        self.q3=q3
        self.q4=q4 
        
        #if q1 == True --> What can i do? 
        if q1: 
            #print ( f"Before tuning kp = {self.kp}, ki = {self.ki}, kd = {self.kd}, Chosse Option 1" )
            self.k1 = self.k1 - self.k1*0.1
            self.tuningPID() 
            if self.debug:
                print ( f"After tuning kp = {self.kp}, ki = {self.ki}, kd = {self.kd}" )
            return self.kp, self.ki, self.kd 

        elif q2: 
            pass 
        elif q3: 
            pass

        #if q2 == True --> What can i do?  
        #if q3 == True --> What can i do? 
        #if q4 == True --> What can i do?   


if __name__ == "__main__": 
    PID = TuningPID()
    PID.loadPIDmodel()
    
    PID.beginTuning(kp=12,ki=12.6,kd=7.6,k1=8.6505,k2=22.4136,k3=0.0439,q1=True)





    #def preProcessData(self):

         




#if torch.cuda.is_available(): 
#    device = torch.device("cuda")
#    modelKp = linearRegression(5, 1)
#    modelKp.load_state_dict(torch.load("models/kp.pt",map_location="cuda:0"), strict=False)
#    modelKp.to(device)
#    print ( "load cuda" )
#else: 
#    modelKp = linearRegression(5, 1)
#    modelKp.load_state_dict(torch.load("models/kp.pt"), strict=False)
## Model class must be defined somewhere
#    #model = torch.load("kp.pt")
##print (modelKp)
##Kp = np.array([8])
##Ki = np.array([9])
##Kd = np.array([10])
##K1 = np.array([11])
##K2 = np.array([12])
##K3 = np.array([13])
#
#xTest = np.array([Kp,Ki,K1,K2,K3],dtype=np.float32).T        
#
#with torch.no_grad(): # we don't need gradients in the testing phase
#    if torch.cuda.is_available(): 
#        predicted = modelKp(Variable(torch.from_numpy(xTest).cuda())).cpu().data.numpy()
#
#    else: 
#
#        predicted = modelKp(Variable(torch.from_numpy(xTest))).data.numpy()
#
#
#    print(predicted)
#    print(xTest)
#
