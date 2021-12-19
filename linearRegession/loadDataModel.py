from BEN_datasetPID import PIDDataset 
import numpy as np 

def getArgMin(value,option): 
    data = []
    for i in range(len(option)):
        data.append(abs(value-float(option[i])))
    data = np.array(data)
    return np.argmin(data)


if __name__ == "__main__": 
    pid = PIDDataset() 
    pid.loadDataset() 
    myYeu = getArgMin(10,pid.k2)
    print ( myYeu )
    print (pid.k1[myYeu]) 
    print (pid.k2[myYeu]) 
    print (pid.k3[myYeu]) 
    print (pid.kp[myYeu]) 
    print (pid.ki[myYeu]) 
    print (pid.kd[myYeu]) 


