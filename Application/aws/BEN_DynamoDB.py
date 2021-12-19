import boto3 
from decimal import * 
from boto3.dynamodb.conditions import Key, Attr 
from datetime import date, datetime


class DynamoDB(): 
    def __init__(self,table1='Device',tabel2='MachineLearning',debug=True): 
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

        # init name tables
        self.nameTableDevice = table1
        self.nameTableML = tabel2 
        #init show debug
        self.debug = debug 
        #config tables in AWS
        dynamodb = boto3.resource('dynamodb')

        self.tableDevice = dynamodb.Table('Device') 
        self.tableML = dynamodb.Table('MachineLearning')
        self.tableApp = dynamodb.Table('App')
        self.tableStorage = dynamodb.Table('Storage')
        #init data send in cloud 
        self.dataDevice = None 
        self.dataML = None
        self.dataApp = None 
        self.dataStorage = None 

    def sendData(self, table=None, id=None, currentID=None, name=None, online=True, 
                 kp=None, ki=None, kd=None, 
                 k1=None, k2=None, k3=None, 
                 sp=None, pv=None, cv=None,  
                 busy=False, stop=False, 
                 moveToPos=False,movePara=False, autoTune=False,
                 setpoint=None,
                 q1=False, q2=False, q3=False, 
                 cvMax=None, cvMin=None, sp1=None, sp2=None,
                 ZN = False, ML = False, status = None
                 ):
        
        if table == "Device": 
            self.dataDevice = {
                "ID": id,
                "Name": name,
                "object": {
                    "online": online,
                    "currentID": currentID,
                    "busy": busy,
                    "PID": {
                        "kp": str(kp),
                        "ki": str(ki),
                        "kd": str(kd)},
                    "quality": {
                        "settlingTime": str(k1),
                        "steadyStateError": str(k3),
                        "overshoot": str(k2)},
                    "parameterPID": {
                        "sp": str(sp),
                        "pv": str(pv),
                        "cv": str(cv)},
                    "time": {
                        "day": self.today(),
                        "time": self.timeNow()}
                }
            }

            self.tableDevice.put_item(Item=self.dataDevice)

        elif table == "ML": 
            self.dataML = {
                "ID": id,
                "Name": name,
                "object": {
                    "online": online,
                    "currentID": currentID,
                    "PID": {
                        "kp": str(kp),
                        "ki": str(ki),
                        "kd": str(kd)},
                    "control": {
                        "controlBit": {
                            "moveToPos":moveToPos,
                            "movePara" :movePara, 
                            "stop":stop,
                            "autoTune":autoTune},
                        "setpoint": str(setpoint)}, 
                    "time": {
                        "day": self.today(),
                        "time": self.timeNow()}
                }
            }

            self.tableML.put_item(Item=self.dataML)

        elif table=="App": 
            self.dataApp = {
                "ID": id,
                "Name": name,
                "object": {
                    "online": online,
                    "PID": {
                        "kp": str(kp), 
                        "ki": str(ki),
                        "kd": str(kd)},
                    "control":{
                        "ZN" : ZN,
                        "ML" : ML,
                        "status": str(status)
                    },
                    "option": {
                        "settlingTime": q1,
                        "steadyStateError": q3,
                        "overshoot": q2},
                    "setting": {
                        "cvMax": str(cvMax),
                        "cvMin": str(cvMin),
                        "sp1": str(sp1),
                        "sp2": str(sp2)
                    },
                    "time": {
                        "day": self.today(),
                        "time": self.timeNow()}
                }
            }
            self.tableApp.put_item(Item=self.dataApp)
            
        elif table=="Stotage": 
            self.dataStorage={
                "ID": id,
                "Name": name,
                "object": {
                    "PID": {
                        "kp": str(kp), 
                        "ki": str(ki),
                        "kd": str(kd)},
                    "quality": {
                        "settlingTime": k1,
                        "steadyStateError": k2,
                        "overshoot": k3},
                    "time": {
                        "day": self.today(),
                        "time": self.timeNow()}
                }
            }
            self.tableStorage.put_item(Item=self.dataStorage)
                                                        





    def receiveData(self,table=None,id=None): 
        if table == "Device":
            response= self.tableDevice.scan(FilterExpression = Attr('ID').eq(id))
            return response["Items"][0]["object"]
        elif table == "ML": 
            response= self.tableML.scan(FilterExpression = Attr('ID').eq(id))
            return response["Items"][0]["object"]
        elif table == "App": 
            response= self.tableApp.scan(FilterExpression = Attr('ID').eq(id))
            return response["Items"][0]["object"]
        elif table == "Stotage": 
            response= self.tableStorage.scan(FilterExpression = Attr('ID').eq(id))
            return response["Items"][0]["object"]
        else:
            return None

    
    def getFinalID(self,table=None): 
        if table == "Device": 
            return self.tableDevice.item_count
        elif table == "ML": 
            return self.tableML.item_count
        elif table == "App": 
            return self.tableApp.item_count
        elif table == "Stotage": 
            return self.tableStorage.item_count
        else: 
            return None 


    def today(self):
        today = date.today()
        day = today.strftime("%B %d, %Y")
        return day

    def timeNow(self): 
        now = datetime.now()
        time= now.strftime("%H:%M:%S")
        return time 

if __name__ == '__main__': 
    cloud = DynamoDB()
    print ( cloud.receiveData(table="App",id=1)) 
    print ( cloud.getFinalID(table="App")) 
    cloud.sendData(table="ML",
                   id=6, currentID= 3, name="Ben Dep Trai",
                   online=True, 
                   kp=3.333,ki=4,kd=5,
                   movePara=False,moveToPos=False,stop=False, autoTune=False,
                   setpoint=3.2)
    cloud.sendData(table="Device",
                   id=6,currentID=3,name="Ben Dep Trai",
                   online=True,
                   busy=False,
                   kp=3.333,ki=4,kd=5,
                   k1=3, k2=3, k3=4,
                   sp=2, pv=4.3, cv=3
                   )
    cloud.sendData(table="App",
                   id=6,name="Ben Dep Trai",
                   online=True, 
                   kp=3.333,ki=4,kd=5,
                   ZN=False,ML=False,status="stop",
                   cvMax = 3, cvMin=3, sp1 = 3, sp2 =3,
                   q1= False, q2= False, q3= False
                   )
    cloud.sendData(table="Stotage",
                   id=6,name="Ben Dep Trai",
                   kp=3.333,ki=4,kd=5,
                   k1=1, k2=2, k3=3
                   )