import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np 
import json 
# PID parameter
class PIDDataset():
    def __init__( self, pathDataset='data/results2.csv' ): 

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

        self.pid = pd.read_csv('data/results2.csv')
        self.pid = np.array(self.pid)
        count = 0  
        for i, pid in enumerate(self.pid): 
            data = json.loads(pid[2])
            #ID = json.loads(pid)
            #print ( res["PID"]["M"]["kp"]["N"] )
            ki = float(data["PID"]["M"]["ki"]["N"])
            check = float(data["quality"]["M"]["overshoot"]["N"]) 
            if check > 50 or check < 1 or ki < 0.004:
                continue
            self.kp = np.append(self.kp,float(data["PID"]["M"]["kp"]["N"]))  
            self.ki = np.append(self.ki,float(data["PID"]["M"]["ki"]["N"]))  
            self.kd = np.append(self.kd,float(data["PID"]["M"]["kd"]["N"]))  

            self.k1 = np.append(self.k1,float(data["quality"]["M"]["settlingTime"]["N"]))  
            self.k2 = np.append(self.k2,float(data["quality"]["M"]["overshoot"]["N"]))  
            self.k3 = np.append(self.k3,float(data["quality"]["M"]["steadyStateError"]["N"]))  
            count += 1
            print (pid[0])
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
    


if __name__ =="__main__": 
    pid = PIDDataset()
    pid.loadDataset()
    x,y = pid.kdDataset()
    print ( x.shape )
    print ( y.shape )
    print ( pid.k2 )
    plt.scatter(pid.kp,pid.k3)
    plt.xlabel('kd')
    plt.ylabel('settlingTime')
    plt.show()

#print (kp.shape) 
#print (ki.shape)
#print (kd.shape)
#
#print (k1.shape)
#print (k2.shape)
#print (k3.shape)
