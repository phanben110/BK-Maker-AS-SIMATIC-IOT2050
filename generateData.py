#Import library custom for Tuining Machine Learning
from linearRegession.BEN_TuningPID import TuningPID as TuningPIDML 
#Import libray custom for send and receive data with AWS 
from aws.BEN_DynamoDB import DynamoDB as cloudAWS 

import time  
from numpy import random 
from random import randint
#------------set up for PID ML---------------
#set up tuning PID ussing Machine learning 
#PID = TuningPIDML(pathKp="linearRegession/models/kp.pt",pathKi="linearRegession/models/ki.pt",pathKd="linearRegession/models/kd.pt",debug=True) 
#load model 
#PID.loadPIDmodel()

#------------set up for cloudAWS ---------------------
cloud = cloudAWS()


#---------Begin tuining--------------------
#kp,ki,kd = PID.beginTuning(kp=12,ki=12.6,kd=7.6,k1=8.6505,k2=22.4136,k3=0.0439,q1=True)
#print ( kp,ki,kd )

#----------Begin interact with cloudAWS--------------
# receive data from cloud aws
print ( "*****BK-MAKER AS TEAM*****" ) 
print ( "*****Set up*****" ) 
dataDevice =  cloud.receiveData(table="Device",id=1)
dataML =  cloud.receiveData(table="ML",id=1)
idDevice = int(dataDevice["currentID"])
setpoint = int(dataML["control"]["setpoint"])

print ( f"current ID: {idDevice}" ) 
print ( f"current setpoint: {setpoint}" ) 
#dataDevice =  cloud.receiveData(table="ML",id=1)
#print (dataDevice)

# get the final ID in the cloud 
#finalID = cloud.getFinalID(table="Device") 

#print (finalID)

#send data to table Machine Learning 
#cloud.sendData(table="MachineLearning",id=26,name="Ben Dep Trai",online=True, kp=3.333,ki=4,kd=5, setPoint=34, controlBit=2)

#send data to table Device 
#cloud.sendData(table="Device",id=26,name="Ben Dep Trai",online=True, kp=3.333,ki=4,kd=5, k1=3.2, k2=3.3, k3=4.3, q1=True)

#cloud.sendData(table="ML",
#               id=1, currentID=None, name="Motor_1",
#               movePara=False,moveToPos=False,stop=False, autoTune=False)
#cloud.sendData(table="Device",
#               id=6,currentID=3,name="Ben Dep Trai",
#               online=True,
#               busy=False,
#               kp=3.333,ki=4,kd=5,
#               k1=3, k2=3, k3=4,
#               sp=2, pv=4.3, cv=3
#               )
#cloud.sendData(table="App",
#               id=6,name="Ben Dep Trai",
#               online=True, 
#               kp=3.333,ki=4,kd=5,
#               ZN=False,ML=False,status="stop",
#               cvMax = 3, cvMin=3, sp1 = 3, sp2 =3,
#               q1= False, q2= False, q3= False
#               )
#cloud.sendData(table="Stotage",
#               id=6,name="Ben Dep Trai",
#               kp=3.333,ki=4,kd=5,
#               k1=1, k2=2, k3=3
#               )
#
Kp = 0.004442581906914711
Kd = 0.0016897942405194044
Ki = 0.0011265295324847102
count = idDevice + 1 
check=False
am = 1
#setpoint = 150
time.sleep(2) 
while True: 
    if setpoint == 150:
        setpoint = 200
    else :
        setpoint = 150
    #setpoint = randint(100,250)
    timeBegin = time.time()
    x=random.rand(3)/8
    #Kp = Kp + Kp*x[0]*am
    #Ki = Ki + Ki*x[1]*am 
    #Kd = Kd + Ki*x[2]*am
    print (f"*****step 1: Current ID: {count}, Kp = {Kp}, Ki = {Ki}, Kd = {Kd}, setpoint: {setpoint}")
    

    currentData = cloud.receiveData(table="Device",id=1)
    settlingTime =  currentData["quality"]["settlingTime"]
    overshoot = currentData["quality"]["overshoot"]

    
    time.sleep(1)
    
    cloud.sendData(table="ML",
                   id=1, currentID=count , name="Motor_1",
                   online=True, 
                   kp=Kp,ki=Ki,kd=Kd,
                   movePara=True,moveToPos=False,stop=False, autoTune=False,
                   setpoint=setpoint)
    print ("*****step 2: set True movePara")
    time.sleep(2)

    cloud.sendData(table="ML",
                   id=1, currentID=count , name="Motor_1",
                   online=True, 
                   kp=Kp,ki=Ki,kd=Kd,
                   movePara=False,moveToPos=False,stop=False, autoTune=False,
                   setpoint=setpoint)
    
    time.sleep(2)

   # cloud.sendData(table="ML",
   #                id=1, currentID=count , name="Motor_1",
   #                online=True, 
   #                kp=Kp,ki=Ki,kd=Kd,
   #                movePara=False,moveToPos=True,stop=False, autoTune=False,
   #                setpoint=setpoint)
   # time.sleep(3)
   # cloud.sendData(table="ML",
   #                id=1, currentID=count , name="Motor_1",
   #                online=True, 
   #                kp=Kp,ki=Ki,kd=Kd,
   #                movePara=False,moveToPos=False,stop=False, autoTune=False,
   #                setpoint=setpoint)
    print ("*****step 3: set False")
    time.sleep(2)

    checkPrint = True  
    while check == False: 
        dataDevice =  cloud.receiveData(table="Device",id=1)
        
        idDevice = int(dataDevice["currentID"]) 
        settlingDevice = dataDevice["quality"]["settlingTime"]
        overshootDevice = dataDevice["quality"]["overshoot"] 
        if checkPrint == True:
            print (f"*****step 4: check currentID=={count} and settlingTime != {settlingTime} and overshoot != {overshoot}")
            print ( f"cloud: currentID: {idDevice}, settlingTime: {settlingDevice}, overshoot: {overshootDevice}" )
            checkPrint = False
        print (".", end="", flush=True)
        time.sleep(0.1)
        if  (idDevice == count) and (settlingDevice != settlingTime) and (overshoot != overshootDevice): 
            check == True 
            print("")
            print ("*****step 5: Prepare for new ID")
            time.sleep(1)

            cloud.sendData(table="ML",
                           id=1, currentID=count , name="Motor_1",
                           online=True, 
                           kp=Kp,ki=Ki,kd=Kd,
                           movePara=False,moveToPos=False,stop=False, autoTune=False,
                           setpoint=setpoint)
            count +=1 
            am = am*(-1)
            break 
    print ( f"-----Done {count} , runing time :{(time.time() - timeBegin)} s-----" )
    print ("")
