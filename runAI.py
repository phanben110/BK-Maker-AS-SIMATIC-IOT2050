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


#---------Begin tuining--------------------
kp,ki,kd = PID.beginTuning(kp=0.027992654591798782,ki=0.009446900337934494,kd=0.03778810054063797,k1=10.200000000000001,k2=7.506209012232492,k3=0.016573547601618034,q1=True)
print ( kp,ki,kd )

#----------Begin interact with cloudAWS--------------
# receive data from cloud aws
#dataDevice =  cloud.receiveData(table="Device",id=1)
#dataDevice =  cloud.receiveData(table="ML",id=1)
#print (dataDevice)
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
