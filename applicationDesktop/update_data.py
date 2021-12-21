from threading import Thread, Event
import os
import csv
import time
from PyQt5.QtCore import QObject,pyqtSignal,pyqtSlot
from aws.BEN_DynamoDB import DynamoDB as cloudAWS 

class update_data(QObject):
    data_available = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.path = "F:\SIEMENS COMPERTITION\Ben\simenAWS\Application"
        self.csvList = []
        self.Kp_motor = 0.0
        self.lastIDFile = 0
        for x in os.listdir():
            if x.endswith(".csv"):
        # list only csv file present in application Folder
                self.csvList.append (x)
        print (self.csvList)
        self.cloud = cloudAWS()
        self.finalID = self.cloud.getFinalID(table="Device") 
        print (self.finalID)
        # Read all object was listed in file Object_name.csv and create a file corresponding to that object
        file = open("Object.csv", mode = "r", encoding= "utf-8-sig")
        header = file.readline ()
        i = 0
        row = file.readline ()
        self.ObjectnameList = [" "]
        while row != "":
            i = i + 1 
            row_list = row.split(",")
            object_name = row_list[1]
            self.ObjectnameList.append (object_name)
            object_file_name = str(object_name) +".csv" 
             # If object had a file, do not create a new file
            if object_file_name not in self.csvList:
                file_object = open (object_file_name ,mode = "w", encoding= "utf-8-sig")
                file_object.write ("ID,KP,KI,KD,Set point, Process Value, Current Value,Overshoot, Settling time,Steady-state error, Day,Time\n")
                file_object.close
            print (row_list)
            print (i)
            row = file.readline ()

        self.thread = None
        self.alive = Event()

    def ObjectLastID (self):
        file_object1 = open ("Motor_1.csv", mode = "r", encoding= "utf-8-sig")
        header = file_object1.readline ()
        row = file_object1.readline () 
        self.lastIDMotor = 0
        while row != "":
            self.lastIDMotor = self.lastIDMotor + 1
            row = file_object1.readline ()
            
       
        
        file_object1.close
    def starThread (self):
        self.thread = Thread (target = self.updateData)
        self.thread.setDaemon(1)
        self.alive.set()
        self.thread.start()


    def updateData (self):
        # while True:
            self.finalID = self.cloud.getFinalID(table="Device") 
            print (self.finalID)
            # self.ObjectLastID()
            self.lastIDMotor = self.lastIDMotor + 1
            while self.lastIDMotor <= self.finalID :
                
                try:
                    dataDevice =  self.cloud.receiveData(table="Device", id=self.lastIDMotor)
                except:
                    self.lastIDMotor = self.lastIDMotor + 1
                PID_Para = dataDevice["PID"]
                Time = dataDevice["time"]
                Quality = dataDevice["quality"]
                parameterPID = dataDevice["parameterPID"]

                self.Kp_motor = float(PID_Para ["kp"])
                self.Ki_motor = float(PID_Para ["ki"])
                self.Kd_motor = float(PID_Para ["kd"])
                self.OV_motor = float(Quality["overshoot"])
                self.ST_motor = float(Quality["settlingTime"])
                self.SSE_motor = float(Quality["steadyStateError"])
                self.SP_motor = float (parameterPID["sp"])
                self.PV_motor = float (parameterPID["pv"])
                self.CV_motor = float (parameterPID["cv"])
                self.Day_motor = str(Time ["day"])
                self.Time_motor = str(Time ["time"])          
                list_data = str(self.lastIDMotor)+','+str(self.Kp_motor) +','+str(self.Ki_motor)+','+str(self.Kd_motor) +','+str(self.SP_motor)+','+str(self.PV_motor)+','+str(self.CV_motor)+','+str(self.OV_motor)+','+str(self.ST_motor)+','+str(self.SSE_motor)+','+str(self.Day_motor)+','+str(self.Time_motor)+'\n'
                self.data_list = list_data
                print (self.Kp_motor)
                print (list_data)
                csvfile = open('Motor_1.csv',mode= 'a')
                if list_data != 0:
                    csvfile.write (list_data)
                    print (dataDevice)
                    self.lastIDMotor = self.lastIDMotor + 1
                    csvfile.close ()
                
    def stop_thread(self):
	    if(self.thread is not None):
		    self.alive.clear()
		    self.thread.join()
		    self.thread = None


