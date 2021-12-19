import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np 
import json 
# PID parameter
class PIDDataset():
    def __init__( self, pathDataset='data/results3.csv' ): 

        self.kp = np.array([])
        self.ki = np.array([])
        self.kd = np.array([]) 
        
        self.k1 = np.array([]) 
        self.k2 = np.array([])
        self.k3 = np.array([])
        
        self.xTrainKp =None  
        self.xTrainKi =None  
        self.xTrainKd =None  

        self.yTrainKp =None  
        self.yTrainKi =None  
        self.yTrainKd =None  

        self.pid = None 

    def loadDataset(self): 

        self.pid = pd.read_csv('data/results3.csv')
        self.pid = np.array(self.pid)
        count = 0  
        for i, pid in enumerate(self.pid): 
            try:
                
                data = json.loads(pid[2])
                #ID = json.loads(pid)
                #print ( res["PID"]["M"]["kp"]["N"] )
                ki = float(data["PID"]["M"]["ki"]["N"])
                kp = float(data["PID"]["M"]["kp"]["N"])

                kd = float(data["PID"]["M"]["kd"]["N"])
                k3 = float(data["quality"]["M"]["steadyStateError"]["N"])
                k2 = float(data["quality"]["M"]["overshoot"]["N"]) 
                k1 = float(data["quality"]["M"]["settlingTime"]["N"]) 
               # if k1 > 20 or k1 < 0.0001:
               #     print ( 1 )
               #     continue
               # if k2 > 20 or k2 < 0.0001:
               #     print (2)
               #     continue
               # if k3 > 20 or k3 < 0.0001: 
               #     print (3)
               #     continue 
               # if kp < 0.0002 or kp > 0.03:
               #     print (4)
               #     continue
               # if kd < 0.0008 or kd > 0.0025:
               #     print (5)
               #     continue
               # if ki < 0.098 or ki > 0.002: 
               #     print (6)
               #     continue

                #if kp > 0.05: 
                #    continue
                if k1 > 10 or k1 < 0.0001:
                    continue
                if k2 > 10 or k2 < 0.0001:
                    continue
                if k3 > 10 or k3 < 0.0001: 
                    continue 
                #if kd < 0.01:
                #    continue
                    
                self.kp = np.append(self.kp,float(data["PID"]["M"]["kp"]["N"]))  
                self.ki = np.append(self.ki,float(data["PID"]["M"]["ki"]["N"]))  
                self.kd = np.append(self.kd,float(data["PID"]["M"]["kd"]["N"]))  

                self.k1 = np.append(self.k1,float(data["quality"]["M"]["settlingTime"]["N"]))  
                self.k2 = np.append(self.k2,float(data["quality"]["M"]["overshoot"]["N"]))  
                self.k3 = np.append(self.k3,float(data["quality"]["M"]["steadyStateError"]["N"]))  
                count += 1
                #print (pid[0])
            except Exception as e: 
                pass
                #print (e)
        print (f"count {count}"  )

    def kpDataset(self): 

        self.xTrainKp = np.array([self.ki, self.kd, self.k1, self.k2, self.k3],dtype=np.float32).T
        self.yTrainKp = np.array(self.kp, dtype=np.float32).reshape(-1,1)

        return self.xTrainKp, self.yTrainKp 

    def kiDataset(self): 

        self.xTrainKi = np.array([self.kp, self.kd, self.k1, self.k2, self.k3],dtype=np.float32).T
        self.yTrainKi = np.array(self.ki, dtype=np.float32).reshape(-1,1)

        return self.xTrainKi, self.yTrainKi 

    def kdDataset(self): 

        self.xTrainKd = np.array([self.kp, self.ki, self.k1, self.k2, self.k3],dtype=np.float32).T
        self.yTrainKd = np.array(self.kd, dtype=np.float32).reshape(-1,1)

        return self.xTrainKd, self.yTrainKd 

    def getArgMin(self,value,option):
        data = []                                       
        for i in range(len(option)):
            data.append(abs(value-float(option[i])))
        data = np.array(data)
        return np.argmin(data)

    def beginTuning(self,K1=None,K2=None,K3=None,q1=False,q2=False,q3=False,k=0.5): 
        if q1 == True: 
            K1 = K1 - k*K1
            argmin = self.getArgMin(K1,self.k1)
            return [self.kp[argmin], self.ki[argmin],self.kd[argmin], self.k1[argmin],self.k2[argmin],self.k3[argmin]]
        elif q2 == True: 
            K2 = K2 - k*K2
            argmin = self.getArgMin(K2,self.k2)
            return [self.kp[argmin], self.ki[argmin],self.kd[argmin], self.k1[argmin],self.k2[argmin],self.k3[argmin]]
        elif q3 == True: 
            K3 = K3 - k*K3
            argmin = self.getArgMin(K3,self.k3)
            return [self.kp[argmin], self.ki[argmin],self.kd[argmin], self.k1[argmin],self.k2[argmin],self.k3[argmin]]



                                                

    


if __name__ =="__main__": 
    pid = PIDDataset()
    pid.loadDataset()
    print (pid.beginTuning(K1=30,q1=True))


   # x,y = pid.kdDataset()
    
    #print ( pid.k1[n] )
    #print ( pid.k2[n] )
    #print ( pid.k3[n] )
    #print ( pid.kp[n] )
    #print ( pid.ki[n] )
    #print ( pid.kd[n] )
    plt.scatter(pid.kd,pid.k3)
    plt.xlabel('kd')
    plt.ylabel('Overshoot')
    plt.show()

#print (kp.shape) 
#print (ki.shape)
#print (kd.shape)
#
#print (k1.shape)
#print (k2.shape)
#print (k3.shape)
