import numpy as np  
import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np  
from neuralNetwork.BEN_model import linearRegression 
import torch 
from torch.autograd import Variable

class TuningPID():
    def __init__ (self,pathKp="models/kp.pt", pathKi="models/ki.pt", pathKd="models/kd.pt", useCuda=True, debug=True): 
        """
        Kp, Ki, Kd : is value of PID 
        K1, K2, K3 : is the value after evaluation 
        Q1, Q2, Q3, Q4 : is the mode slection 
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

    def beginTuning(self,kp,ki,kd,k1,k2,k3,q1=False,q2=False,q3=False,q4=False): 
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
        
        # if q1 
        # if q2 
        # if q3 
        # if q4  
        self.preProcessData()
        kp = self.predicted(self.modelKp, self.xTestKp )
        print ( kp  )
        print ( self.xTestKp )


if __name__ == "__main__": 
    PID = TuningPID()
    PID.loadPIDmodel()
    
    PID.beginTuning(12,12.6,7.6,8.6505,22.4136,0.0439)





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
