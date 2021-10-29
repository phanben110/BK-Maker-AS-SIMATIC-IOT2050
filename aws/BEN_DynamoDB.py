#import  some library 
#define 

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
        #init data send in cloud 
        self.dataDevice = None 
        self.dataML = None 

    def sendData(self, table=None, id=None, name=None, online=True, 
                 kp=None, ki=None, kd=None, 
                 k1=None, k2=None, k3=None, 
                 q1=False, q2=False, q3=False, q4=False, 
                 setPoint=None, controlBit=None
                 ):
        
        if table == "Device": 
            self.dataDevice = {
                "ID": id,
                "Name": name,
                "Object": {
                    "Online": online,
                    "PID": {
                        "Kp": str(kp),
                        "ki": str(ki),
                        "Kd": str(kd)},
                    "Quality": {
                        "Settling time": str(k1),
                        "Steady-state error": str(k3),
                        "Overshoot": str(k2)},
                    "Setting": {
                        "Max Settling time": q1,
                        "Max Overshoot": q2,
                        "Max Steady-state error": q3},
                    "Time": {
                        "Day": self.today(),
                        "Time": self.timeNow()}
                }
            }

            self.tableDevice.put_item(Item=self.dataDevice)

        elif table == "ML" or "MachineLearning": 
            self.dataML = {
                "ID": id,
                "Name": name,
                "Object": {
                    "Online": online,
                    "PID": {
                        "Kp": str(kp),
                        "ki": str(ki),
                        "Kd": str(kd)},
                    "Control": {
                        "Set point": str(setPoint),
                        "Control bit": str(controlBit)},
                    "Quality": {
                        "Settling time": str(k1),
                        "Steady-state error": str(k3),
                        "Overshoot": str(k2)}, 
                    "Time": {
                        "Day": self.today(),
                        "Time": self.timeNow()}
                }
            }

            self.tableML.put_item(Item=self.dataML)


    def receiveData(self,table=None,id=None): 
        if table == "device" or "Device":
            response= self.tableDevice.scan(FilterExpression = Attr('ID').eq(id))
            return response["Items"][0]["Object"]
        elif table == "ML" or "MachineLearning": 
            response= self.tableML.scan(FilterExpression = Attr('ID').eq(id))
            return response["Items"][0]["Object"]
        else:
            return None

    
    def getFinalID(self,table=None): 
        if table == "device" or "Device": 
            return self.tableDevice.item_count
        elif table == "ML" or "MachineLearning": 
            return self.dataML.item_count
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
    print ( cloud.receiveData(table="Device",id=1)) 
    print ( cloud.getFinalID(table="Device")) 
    print ( cloud.sendData(table="MachineLearning",id=26,name="Ben Dep Trai",online=True, kp=3.333,ki=4,kd=5, setPoint=34, controlBit=2) )
    print ( cloud.sendData(table="Device",id=26,name="Ben Dep Trai",online=True, kp=3.333,ki=4,kd=5, k1=3.2, k2=3.3, k3=4.3, q1=True) )
