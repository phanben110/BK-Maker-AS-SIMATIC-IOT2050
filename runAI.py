#Import library custom for Tuining Machine Learning
from linearRegession.BEN_TuningPID import TuningPID as TuningPIDML 
#Import libray custom for send and receive data with AWS 
from aws.BEN_DynamoDB import DynamoDB as cloudAWS 

import time  
from numpy import random 
from random import randint
#------------set up for PID ML---------------
#set up tuning PID ussing Machine learning 
PID = TuningPIDML(pathKp="linearRegession/models/kp.pt",pathKi="linearRegession/models/ki.pt",pathKd="linearRegession/models/kd.pt",debug=True) 
#load model 
PID.loadPIDmodel()

#------------set up for cloudAWS ---------------------
cloud = cloudAWS()


#finalID = cloud.getFinalID(table="App") 
#----------Begin interact with cloudAWS--------------
# receive data from cloud aws
dataApp =  cloud.receiveData(table="App",id=1)
dataML =  cloud.receiveData(table="ML",id=1)
dataDevice =  cloud.receiveData(table="Device",id=1)

Kp = float(dataApp["PID"]["kp"])
Ki = float(dataApp["PID"]["ki"])
Kd = float(dataApp["PID"]["kd"])

K1 = float(dataDevice["quality"]["settlingTime"])
K2 = float(dataDevice["quality"]["overshoot"])
K3 = float(dataDevice["quality"]["steadyStateError"] )

Q1 = bool(dataApp["option"]["settlingTime"])
Q2 = bool(dataApp["option"]["overshoot"])
Q3 = bool(dataApp["option"]["steadyStateError"])

setpoint = int(dataML["control"]["setpoint"])

if setpoint == 150: 
    setpoint = 200
else : 
    setpoint = 150

idDevice = int(dataDevice["currentID"]) 
print (f"Kp: {Kp}, Ki: {Ki}, Kd: {Kd}, K1: {K1}, K2: {K2}, K3: {K3}, Q1: {Q1}, Q2: {Q2}, Q3: {Q3}, ID: {idDevice}, setpoint: {setpoint}")



#---------Begin tuining--------------------
cloud.sendData(table="App",
               id=1,name="Motor",
               online=True, 
               kp=Kp,ki=Ki,kd=Kd,
               ZN=False,ML=False,status="ML Runing...",
               cvMax = 3, cvMin=3, sp1 = 3, sp2 =3,
               q1= False, q2= False, q3= False
               )

mlKp,mlKi,mlKd = PID.beginTuning(kp=Kp,ki=Ki,kd=Kd,k1=K1,k2=K2,k3=K3,q1=Q1, q2=Q2, q3=Q3)
print ( mlKp, mlKi, mlKd )



cloud.sendData(table="ML",
               id=1, currentID=idDevice+1 , name="Motor_1",
               online=True, 
               kp=mlKp,ki=mlKi,kd=mlKd,
               movePara=True,moveToPos=False,stop=False, autoTune=False,
               setpoint=setpoint)
print ("---------------send step 1---------------")
time.sleep(2)


cloud.sendData(table="ML",
               id=1, currentID=idDevice +1  , name="Motor_1",
               online=True, 
               kp=mlKp,ki=mlKi,kd=mlKd,
               movePara=False,moveToPos=False,stop=False, autoTune=False,
               setpoint=setpoint)
print ("---------------send step 1---------------")
time.sleep(2)




cloud.sendData(table="App",
               id=1,name="Motor",
               online=True, 
               kp=Kp,ki=Ki,kd=Kd,
               ZN=False,ML=False,status="Done",
               cvMax = 3, cvMin=3, sp1 = 3, sp2 =3,
               q1= False, q2= False, q3= False
               )

print ( "Done" )





#cloud.sendData(table="App",
#               id=1,name="Motor",
#               online=True, 
#               kp=Kp,ki=Ki,kd=Kd,
#               ZN=False,ML=False,status="ML Runing...",
#               cvMax = 3, cvMin=3, sp1 = 3, sp2 =3,
#               q1= False, q2= False, q3= False
#               )
#

## get the final ID in the cloud 
#finalID = cloud.getFinalID(table="Device") 
#print (finalID)
#
#Kp = 0.03999999910593033
#Kd = 0.03999999910593033
#Ki = 0.001500000013038516
#count = 0
#check=False
#while True: 
#    setpoint = randint(100,250)
#    x=random.rand(3)/2
#    Kp = Kp + Kp*x[0]
#    Ki = Ki + Ki*x[1]
#    Kd = Kd + Ki*x[2]
#    print (f"Current ID: {count}, Kp = {Kp}, Ki = {Ki}, Kd = {Kd}, setpoint: {setpoint}")
#    
#    settlingTime =  cloud.receiveData(table="Device",id=1)["quality"]["settlingTime"]
#    
#    time.sleep(1)
#    
#    cloud.sendData(table="ML",
#                   id=1, currentID=count , name="Motor_1",
#                   online=True, 
#                   kp=Kp,ki=Ki,kd=Kd,
#                   movePara=True,moveToPos=False,stop=False, autoTune=False,
#                   setpoint=setpoint)
#    print ("---------------send step 1---------------")
#    time.sleep(2)
#
#    cloud.sendData(table="ML",
#                   id=1, currentID=count , name="Motor_1",
#                   online=True, 
#                   kp=Kp,ki=Ki,kd=Kd,
#                   movePara=False,moveToPos=False,stop=False, autoTune=False,
#                   setpoint=setpoint)
#    
#    time.sleep(2)
#
#    print ("---------------send step 2---------------")
#    time.sleep(2)
#    if setpoint >= 266 : 
#        setpoint = 126
#
#    
#    while check == False: 
#        dataDevice =  cloud.receiveData(table="Device",id=1)
#        
#        idDevice = int(dataDevice["currentID"]) 
#        settlingDevice = dataDevice["quality"]["settlingTime"]
#        print (f"---------------check currentID=={count} and settling time != {settlingTime} step 3---------------")
#        print ( idDevice, settlingDevice )
#        if  settlingDevice != settlingTime : 
#            check == True 
#            print ("---------------step 3 is OK---------------")
#            time.sleep(1)
#
#            cloud.sendData(table="ML",
#                           id=1, currentID=count , name="Motor_1",
#                           online=True, 
#                           kp=Kp,ki=Ki,kd=Kd,
#                           movePara=False,moveToPos=False,stop=False, autoTune=False,
#                           setpoint=setpoint)
#            count +=1 
#            break 
#    print ( f"Done {count}" )
