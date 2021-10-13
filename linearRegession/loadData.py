import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
lm = LinearRegression()

kp = pd.read_csv('data/kp.txt', sep = "\t")
kp = np.array(kp).T

ki = pd.read_csv("data/ki.txt", sep = "\t")
ki = np.array(ki).T 

kd = pd.read_csv("data/kd.txt", sep = "\t")         
kd = np.array(kd).T 

print ( kp.shape  )
#print ( ki.shape )
#print (kd.shape )
#my = kp 
#kp1 = kp + np.random.normal(0, 0.01, kp.shape) 
#kp2 = kp + np.random.normal(0, .02, kp.shape)
#my = my + kp1 + kp2
#print (my.shape)
Y = kp[0]
X = np.array([kp[1],kp[2],kp[3],kp[4],kp[5]]).T
xTrain, xTest, yTrain, yTest = train_test_split(X,Y, test_size= 0.2, random_state =101)

print (X.shape)
print (Y.shape)

lm.fit(xTrain, yTrain)

print('Coefficients: \n', lm.coef_)


predictions = lm.predict(xTest)
print ( predictions )
print ( yTest )
#plt.scatter(kp[0], kp[3])
#plt.xlabel('Time (hr)')
#plt.ylabel('Position (km)')
#plt.show()
