#Import library custom for Tuining Machine Learning
from linearRegession.BEN_TuningPID import TuningPID as TuningPIDML 
#Import libray custom for send and receive data with AWS 
from aws.BEN_DynamoDB import DynamoDB as cloudAWS 
print ("***BK-MAKER AS Team")

import time  
from numpy import random 
from random import randint
#------------set up for PID ML---------------
#set up tuning PID ussing Machine learning 

PID = TuningPIDML(pathKp="linearRegession/models/kp.pt",pathKi="linearRegession/models/ki.pt",pathKd="linearRegession/models/kd.pt",debug=True) 
#load model 

print ("***Load model AI...")
PID.loadPIDmodel()

#------------set up for cloudAWS ---------------------
cloud = cloudAWS()

def setpointCalc():
    dataML =  cloud.receiveData(table="ML",id=1)
    setpointV = int(dataML["control"]["setpoint"])
    if setpointV == 150: 
        setpointV = 200
    else : 
        setpointV = 150
    return setpointV

def sendDataAutotune(idDevice,status,kp,ki,kd,pid=False):
    if pid == False:
        setpoint = setpointCalc()
        cloud.sendData(table="App",
                       id=1,name="Motor",
                       online=True, 
                       kp=kp,ki=ki,kd=kd,
                       ZN=False,ML=False,status=str(status),
                       cvMax = 3, cvMin=3, sp1 = 3, sp2 =3,
                       q1= False, q2= False, q3= False)

        time.sleep(2)

        cloud.sendData(table="ML",
                       id=1, currentID=int(idDevice)+1  , name="Motor_1",
                       online=True, 
                       kp=kp,ki=ki,kd=kd,
                       movePara=False,moveToPos=False,stop=False,autoTune=True,
                       setpoint=setpoint)
        time.sleep(2)

        cloud.sendData(table="ML",
                       id=1, currentID=int(idDevice) +1  , name="Motor_1",
                       online=True, 
                       kp=kp,ki=ki,kd=kd,
                       movePara=True,moveToPos=False,stop=False,autoTune=True,
                       setpoint=setpoint)
        time.sleep(2)

        cloud.sendData(table="ML",
                       id=1, currentID=int(idDevice) +1  , name="Motor_1",
                       online=True, 
                       kp=kp,ki=ki,kd=kd,
                       movePara=False,moveToPos=False,stop=False,autoTune=False,
                       setpoint=setpoint)
        time.sleep(1)
    else:
        setpoint = setpointCalc()
        cloud.sendData(table="App",
                       id=1,name="Motor",
                       online=True, 
                       kp=kp,ki=ki,kd=kd,
                       ZN=False,ML=False,status=str(status),
                       cvMax = 3, cvMin=3, sp1 = 3, sp2 =3,
                       q1= False, q2= False, q3= False)

        time.sleep(2)

        cloud.sendData(table="ML",
                       id=1, currentID=int(idDevice)+1  , name="Motor_1",
                       online=True, 
                       kp=kp,ki=ki,kd=kd,
                       movePara=True,moveToPos=False,stop=False,autoTune=False,
                       setpoint=setpoint)
        time.sleep(2)

        cloud.sendData(table="ML",
                       id=1, currentID=int(idDevice) +1  , name="Motor_1",
                       online=True, 
                       kp=kp,ki=ki,kd=kd,
                       movePara=False,moveToPos=False,stop=False,autoTune=False,
                       setpoint=setpoint)
        time.sleep(1)




#finalID = cloud.getFinalID(table="App") 
#----------Begin interact with cloudAWS--------------
# receive data from cloud aws
check = True
statusZN0=True
statusZN1=True 
statusZN2=True
statusZN3=True
statusZN4=True

while True :
    if check:
        print ("***Step 1: Get data from DynamoDB AWS")
        print ("***Step 2: Waiting signal from app...")
    else: 
        print (".", end="", flush=True)
        time.sleep(0.1)

    dataApp =  cloud.receiveData(table="App",id=1)
    dataML =  cloud.receiveData(table="ML",id=1)
    dataDevice =  cloud.receiveData(table="Device",id=1)

    cuKp = float( dataDevice["PID"]["kp"])
    cuKi = float( dataDevice["PID"]["ki"])
    cuKd = float( dataDevice["PID"]["kd"])

    idDevice = int(dataDevice["currentID"]) 

    runML = bool(dataApp["control"]["ML"])
    runZN = bool(dataApp["control"]["ZN"])

    if runML == True and runZN == False: 
        check = False
        Q1 = bool(dataApp["option"]["settlingTime"])
        Q2 = bool(dataApp["option"]["overshoot"])
        Q3 = bool(dataApp["option"]["steadyStateError"])
        if Q1 or Q2 or Q3: 
            check = True
            print ("***Step 2: Begin tuning by Machine Learning")
            Kp = float(dataApp["PID"]["kp"])
            Ki = float(dataApp["PID"]["ki"])
            Kd = float(dataApp["PID"]["kd"])
            
            K1 = float(dataDevice["quality"]["settlingTime"])
            K2 = float(dataDevice["quality"]["overshoot"])
            K3 = float(dataDevice["quality"]["steadyStateError"] )
            setpoint = setpointCalc()

            print (f"Kp: {Kp}, Ki: {Ki}, Kd: {Kd}, K1: {K1}, K2: {K2}, K3: {K3}, Q1: {Q1}, Q2: {Q2}, Q3: {Q3}, ID: {idDevice}, setpoint: {setpoint}")
            
            #---------Begin tuining--------------------
            cloud.sendData(table="App",
                           id=1,name="Motor",
                           online=True, 
                           kp=Kp,ki=Ki,kd=Kd,
                           ZN=False,ML=False,status="MLBegin",
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
            print ("***Step 3: Control IoT2050")
            time.sleep(2)
            
            cloud.sendData(table="ML",
                           id=1, currentID=idDevice +1  , name="Motor_1",
                           online=True, 
                           kp=mlKp,ki=mlKi,kd=mlKd,
                           movePara=False,moveToPos=False,stop=False, autoTune=False,
                           setpoint=setpoint)
            time.sleep(2)

            cloud.sendData(table="App",
                           id=1,name="Motor",
                           online=True, 
                           kp=Kp,ki=Ki,kd=Kd,
                           ZN=False,ML=False,status="Done",
                           cvMax = 3, cvMin=3, sp1 = 3, sp2 =3,
                           q1= False, q2= False, q3= False
                           )
            print ("**Step 4: Send status")
            
            print ( "Done" )
    elif runZN == True and runML == False: 
        setpoint = setpointCalc()
        if check:
            print("***Step 2:Begin tuning PID by ZN")
            print (f"ID: {idDevice}, setpoint: {setpoint}")

        print("\r\n***step 3: ZN Begin...")
        sendDataAutotune(idDevice,"ZNTime0",cuKp,cuKi,cuKd)


        check = False
        while statusZN1: 
            data1 = cloud.receiveData(table="Device",id=1)

            K11 = float(data1["quality"]["settlingTime"])
            K21 = float(data1["quality"]["overshoot"])

            kp1 = float( data1["PID"]["kp"])
            ki1 = float( data1["PID"]["ki"])
            kd1 = float( data1["PID"]["kd"])

            if cuKd != kd1 and cuKi != ki1: 
                print("\r\n***step 3: ZN time 1 ...")

                Ku = kp1/0.6
                Tu = 1.2*Ku/ki1

                Kp_PI = 0.7*Ku
                Ki_PI = 1.75*Ku/Tu
                Kd_PI = 0.105*Ku*Tu

                sendDataAutotune(idDevice,"ZNTime1",Kp_PI,Ki_PI,Kd_PI,pid=True)
                #run 
                break 
        while statusZN2: 
            data2 = cloud.receiveData(table="Device",id=1)

            K12 = float(data2["quality"]["settlingTime"])
            K22 = float(data2["quality"]["overshoot"])


            if K11 != K12 and K21 != K22:
                print("\r\n***step 4: ZN time 2 ...")

                kp2 = float( data2["PID"]["kp"])
                ki2 = float( data2["PID"]["ki"])
                kd2 = float( data2["PID"]["kd"])

                Ku = kp2/0.6
                Tu = 1.2*Ku/ki2

                Kp_SO = Ku/3
                Ki_SO = (2/3)*Ku/Tu
                Kd_SO = (1/9)*Ku/Tu
                sendDataAutotune(idDevice,"ZNTime2",Kp_SO,Ki_SO,Kd_SO,pid=True)
                break  

        while statusZN3: 
            data3 = cloud.receiveData(table="Device",id=1)

            K13 = float(data3["quality"]["settlingTime"])
            K23 = float(data3["quality"]["overshoot"])

            
            if K12 != K13 and K22 != K23:
                print("\r\n***step 5: ZN time 3 ...")

                kp3 = float( data3["PID"]["kp"])
                ki3 = float( data3["PID"]["ki"])
                kd3 = float( data3["PID"]["kd"])

                #run 
                Ku = kp3/0.6
                Tu = 1.2*Ku/ki3

                Kp_NO = 0.2*Ku
                Ki_NO = (2/5)*Ku/Tu
                Kd_NO = (1/15)*Ku/Tu

                sendDataAutotune(idDevice,"ZNTime3",Kp_NO,Ki_NO,Kd_NO,pid=True)
                break 

        while statusZN4:
            data4 = cloud.receiveData(table="Device",id=1)

            K14 = float(data4["quality"]["settlingTime"])
            K24 = float(data4["quality"]["overshoot"])

            if K13 != K14 and K23 != K24:
                kp4 = float( data4["PID"]["kp"])
                ki4 = float( data4["PID"]["ki"])
                kd4 = float( data4["PID"]["kd"])
                cloud.sendData(table="App",
                               id=1,name="Motor",
                               online=True, 
                               kp=kp4,ki=ki4,kd=kd4,
                               ZN=False,ML=False,status="ZNDone",
                               cvMax = 3, cvMin=3, sp1 = 3, sp2 =3,
                               q1= False, q2= False, q3= False)

                print("\r\n***Done!")

                print("\r\n----------------------------------------------------------\r\n")

                check = True
                break

    else: 
        if check : 
            print("Please chose method to tuining PID!")

        check = False



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
