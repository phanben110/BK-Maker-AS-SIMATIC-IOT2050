import sys 
from PyQt5.QtWidgets import QMainWindow,QApplication
from ui_v2 import *
from update_data import update_data  
from threading import Thread, Event
import time
import os
from PyQt5 import QtCore, QtWidgets,QtGui
from PyQt5 import uic
from aws.BEN_DynamoDB import DynamoDB as cloudAWS 
import matplotlib.pyplot as plt
from PyQt5.QtGui import QPixmap

plt.subplots_adjust(
        top=0.98,
        bottom=0.095,
        left=0.065,
        right=0.995,
        hspace=0.2,
        wspace=0.2
)

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.UpdateData = update_data() 
        self.cloud = cloudAWS()
        # self.UpdateData.ObjectLastID ()
        self.thread={}    
        self.BitSaveData = False 
        self.ZN_Kp_list = [0,0,0,0,0]
        self.ZN_Ki_list =[0,0,0,0,0]
        self.ZN_Kd_list = [0,0,0,0,0]
        self.ZN_ST_list =[0,0,0,0,0]
        self.ZN_OV_list =[0,0,0,0,0]
        self.ZN_SSE_list = [0,0,0,0,0]
        self.ObjectLastID()
        self.intit_data_chart ()

        #11/23 Cập nhật các giá trị cuối cùng khi khởi động ứng dụng
        self.last_Kp = 0.0
        self.last_Ki = 0.0
        self.last_Kp = 0.0
        self.last_SP = 0.0
        self.last_CV = 0.0
        self.last_PV = 0.0
        self.last_ST = 0.0
        self.last_OV = 0.0
        self.last_SSE = 0.0
        self.Previous_Time = 0.0
        # Bit che do Zn
        self.ZN_mode = False
        self.ML_mode = False
        self.ZN_counter = 0
        self.Stardata = False
        self.Pre_status = ''
        self.status =''
        self.one = False

        #Update object
        self.ui.Name_OB1.addItems(self.UpdateData.ObjectnameList)
        self.ui.OB_select1.addItems(self.UpdateData.ObjectnameList)
        self.ui.OB_select2.addItems(self.UpdateData.ObjectnameList)

        #Event
        self.ui.pushButton.clicked.connect (self.start_worker_1)
        self.ui.OB_select1.activated.connect (self.Autotune_update_object)
        self.ui.OB_select2.activated.connect (self.Advanced_Autotune_update_object)
        self.ui.BT_Begn_Autotune.clicked.connect (self.PID_Autotune_Send)
        self.ui.BT_Begin_Autotune2.clicked.connect (self.Advanced_PID_Autotune_Send)
        self.ui.Update_PID_Para1.clicked.connect (self.ZN_Update_Parameter)
        self.ui.Update_PID_Para2.clicked.connect (self.ML_Update_Parameter)
        # if self.ui.C_PID_Check.isChecked == True :
        #     self.Show_ZN_Classic ()
        # self.ui.C_PID_Check.activated.connect (self.Show_ZN_Classic)    
        

    def PID_Autotune_Send (self):
        finalID = self.cloud.getFinalID(table="App")
        print ('Final App ID:', finalID)
        
        # Lưu lai cac gia trị truoc khi ZN autotune để so sánh
        self.ZN_Kp_list [0] = self.ui.OB_Kp1.value()
        self.ZN_Ki_list [0] = self.ui.OB_Ki1.value()
        self.ZN_Kd_list [0] = self.ui.OB_Kd1.value()
        self.ZN_ST_list [0] = self.ui.SL_OB1.value()
        self.ZN_OV_list [0] = self.ui.OS_OB1.value()
        self.ZN_SSE_list [0] = self.ui.SSE_OB1.value()

        
        # 23/11 bật chế độ ZN mode
        self.ZN_mode = True

        # Gửi dữ liệu lên App
        Kp = self.ui.OB_Kp1.value()
        Ki = self.ui.OB_Ki1.value()
        Kd = self.ui.OB_Kd1.value()
        CvMAX = self.ui.Max_CV1.value ()
        CvMin = self.ui.Min_CV1.value ()
        SP1 = self.ui.SP1_1.value ()
        SP2 = self.ui.SP2_2.value ()

        self.cloud.sendData (table="App",
                       id= 1,name="Motor",
                       online=True, 
                       ZN = True, ML = False,
                       cvMax= CvMAX, cvMin= CvMin, sp1= SP1, sp2 =SP2,
                       kp= Kp,ki=Ki,kd=Kd,
                       q1=False, q2=False, q3= False,
    
         
        )

    def ZN_Update_Parameter (self):
        # print ('_______Da nhan nut___')
        # print (self.ui.C_PID_Check.isChecked())
        if (self.ui.C_PID_Check.isChecked () == True):
            print ('______________ClassicPID____________________')
            self.ui.Cal_Ki1.setText ('Ki ='+ str(self.ZN_Ki_list[3]))
            self.ui.Cal_Kp1.setText ('Kp ='+ str(self.ZN_Kp_list[3]))
            self.ui.Cal_Kd1.setText ('Kd ='+ str(self.ZN_Kd_list[3]))
            self.ui.QC_ST1.setText ('Settling time (s) ='+str(self.ZN_ST_list[3]))
            self.ui.QC_OS1.setText ('Over shoot (%) ='+str(self.ZN_OV_list[3]))
            self.ui.QC_SSA1.setText ('Steady-state error (%) ='+str(self.ZN_SSE_list[3]))
            qpimap = QPixmap('Classic_PID.png')
            self.ui.LB_image_PID_Autotune.setPixmap(qpimap)

        if (self.ui.PI_PID_Check.isChecked() == True):
            print ('_____________PI_PID_____________________')
            self.ui.Cal_Ki1.setText ('Ki ='+ str(self.ZN_Ki_list[2]))
            self.ui.Cal_Kp1.setText ('Kp ='+ str(self.ZN_Kp_list[2]))
            self.ui.Cal_Kd1.setText ('Kd ='+ str(self.ZN_Kd_list[2]))
            self.ui.QC_ST1.setText ('Settling time (s) ='+str(self.ZN_ST_list[2]))
            self.ui.QC_OS1.setText ('Over shoot (%) ='+str(self.ZN_OV_list[2]))
            self.ui.QC_SSA1.setText ('Steady-state error (%) ='+str(self.ZN_SSE_list[2]))
            qpimap = QPixmap('PI_PID.png')
            self.ui.LB_image_PID_Autotune.setPixmap(qpimap)

        if (self.ui.SO_PID_Check.isChecked() == True):

            print ('_______________SO_PID_____________')
            self.ui.Cal_Ki1.setText ('Ki ='+ str(self.ZN_Ki_list[1]))
            self.ui.Cal_Kp1.setText ('Kp ='+ str(self.ZN_Kp_list[1]))
            self.ui.Cal_Kd1.setText ('Kd ='+ str(self.ZN_Kd_list[1]))
            self.ui.QC_ST1.setText ('Settling time (s) ='+str(self.ZN_ST_list[1]))
            self.ui.QC_OS1.setText ('Over shoot (%) ='+str(self.ZN_OV_list[1]))
            self.ui.QC_SSA1.setText ('Steady-state error (%) ='+str(self.ZN_SSE_list[1]))
            qpimap = QPixmap('SO_PID.png')
            self.ui.LB_image_PID_Autotune.setPixmap(qpimap)

        if (self.ui.NO_PID_Check.isChecked() == True):

            print ('_______________NO_PID_____________')
            self.ui.Cal_Ki1.setText ('Ki ='+ str(self.ZN_Ki_list[0]))
            self.ui.Cal_Kp1.setText ('Kp ='+ str(self.ZN_Kp_list[0]))
            self.ui.Cal_Kd1.setText ('Kd ='+ str(self.ZN_Kd_list[0]))
            self.ui.QC_ST1.setText ('Settling time (s) ='+str(self.ZN_ST_list[0]))
            self.ui.QC_OS1.setText ('Over shoot (%) ='+str(self.ZN_OV_list[0]))
            self.ui.QC_SSA1.setText ('Steady-state error (%) ='+str(self.ZN_SSE_list[0]))
            qpimap = QPixmap('NO_PID.png')
            self.ui.LB_image_PID_Autotune.setPixmap(qpimap)

        
    def Advanced_PID_Autotune_Send (self):
        finalID = self.cloud.getFinalID(table="App")
        print ('Final App ID:', finalID)

        # Lưu lai cac gia trị truoc khi ZN autotune để so sánh
        self.ZN_Kp_list [0] = self.ui.OB_Kp1.value()
        self.ZN_Ki_list [0] = self.ui.OB_Ki1.value()
        self.ZN_Kd_list [0] = self.ui.OB_Kd1.value()
        self.ZN_ST_list [0] = self.ui.SL_OB1.value()
        self.ZN_OV_list [0] = self.ui.OS_OB1.value()
        self.ZN_SSE_list [0] = self.ui.SSE_OB1.value()

        self.ML_mode = True

        Kp = self.ui.OB_Kp2.value()
        Ki = self.ui.OB_Ki2.value()
        Kd = self.ui.OB_Kd2.value()
        CvMAX = self.ui.Max_CV2.value ()
        CvMin = self.ui.MinCV_2.value ()
        SP1 = self.ui.SP1_2.value ()
        SP2 = self.ui.SP2_2.value ()


        self.cloud.sendData (table="App",
                       id=1,name="Motor",
                       online=True, 
                       ZN = False, ML = True,
                       cvMax= CvMAX, cvMin= CvMin, sp1= SP1, sp2 =SP2,
                       kp= Kp,ki=Ki,kd=Kd,
                       q1=self.ui.Pri_ST.isChecked(), q2=self.ui.Pri_OS.isChecked(), q3= self.ui.Pri_SSE.isChecked(), 
        )
        
    def ML_Update_Parameter (self):

        self.ui.Cal_Ki2.setText ('Ki ='+ str(self.ZN_Ki_list[0]))
        self.ui.Cal_Kp2.setText ('Kp ='+ str(self.ZN_Kp_list[0]))
        self.ui.Cal_Kd2.setText ('Kd ='+ str(self.ZN_Kd_list[0]))
        self.ui.QC_ST2.setText ('Settling time (s) ='+str(self.ZN_ST_list[0]))
        self.ui.QC_OS2.setText ('Over shoot (%) ='+str(self.ZN_OV_list[0]))
        self.ui.QC_SSE2.setText ('Steady-state error (%) ='+str(self.ZN_SSE_list[0]))
        qpimap = QPixmap('ML_PID.png')
        self.ui.LB_image_PID_Ad_autotune.setPixmap(qpimap)        

    def Show_ZN_Classic (self):
        print ('________Begin_____________')
        self.ui.Cal_Ki1.setText ('Ki ='+ str(self.ZN_Ki_list[1]))
        self.ui.Cal_Kp1.setText ('Kp ='+ str(self.ZN_Kp_list[1]))
        self.ui.Cal_Kd1.setText ('Kd ='+ str(self.ZN_Kd_list[1]))
        self.ui.QC_ST1.setText ('Settling time (s) ='+str(self.ZN_ST_list[1]))
        self.ui.QC_OS1.setText ('Over shoot (%) ='+str(self.ZN_OV_list[1]))
        self.ui.QC_SSA1.setText ('Steady-state error (%) ='+str(self.ZN_SSE_list[1]))
        qpimap = QPixmap('ZNTime1.png')
        self.ui.LB_image_PID_Autotune.setPixmap(qpimap)

    def start_worker_1(self):
        # 23/11 Khi bắt đầu cập nhật những dữ liệu cuối cùng trong file CSV
        self.ui.PV_OB1.display(self.last_PV) 
        self.ui.CV_OB1.display (self.last_CV)
        self.ui.SV_OB1.display(self.last_SP)
        self.ui.SL_OB1.display(self.last_ST)
        self.ui.OS_OB1.display(self.last_OV)    
        self.ui.SSE_OB1.display(self.last_SSE)    
        
        # bat đầu luồn thứ 2
        self.thread[1] = ThreadClass(parent=None,index=1)
        self.thread[1].start()
        self.thread[1].any_signal.connect(self.my_function)
        self.ui.Online_Check_OB1.setCheckState(True)
        
    def stop_worker_1(self):
        self.thread[1].stop()
        
    
    def intit_data_chart (self):
        file = open("Motor.csv", mode = "r", encoding= "utf-8-sig")
        header = file.readline () 
        lastIDMotor = 0
        lastSetPoint = 0
        row = file.readline ()
        while row != "":
            lastIDMotor = lastIDMotor + 1
            row_list = row.split(",")
            lastSetPoint = row_list[4]
            self.lastPosition = row_list[6]

            #23/11 Cập nhật các giá trị cuối cùng
            self.last_SP = row_list [4]
            self.last_CV = row_list [6]
            self.last_PV = row_list [5]
            self.last_ST = row_list [8]
            self.last_OV = row_list [7]
            self.last_SSE = row_list [9]

            row = file.readline ()
        print (lastIDMotor)   
        print (lastSetPoint)
        print (self.lastPosition)
        # print ('1:',self.last_SP)
        # print ('2:',self.last_CV)
        # print ('3:',self.last_PV)
        # print ('4:',self.last_ST)
        # print ('5:',self.last_OV)
        # print ('6:',self.last_SSE)

        file.close()

        file = open("Motor.csv", mode = "r", encoding= "utf-8-sig")
        header = file.readline ()
        row2 = file.readline ()
        while row2 !="":
            row_list2 = row2.split(",")
            currentSetPoint = row_list2 [4]
            if currentSetPoint == lastSetPoint :
                self.Yaxis.append (float(row_list2[6]))
                self.Xaxis.append (float(row_list2[11]))
            else :
                self.Yaxis =[]
                self.Xaxis=[]
            row2 = file.readline () 
        print (self.Yaxis)
        print (self.Xaxis)
        file.close()

        self.SetPoint = [float(lastSetPoint),float(lastSetPoint)]
        self.TimeSetPoint = [min(self.Xaxis),max(self.Xaxis)]
        plt.plot (self.Xaxis,self.Yaxis)
        plt.plot (self.TimeSetPoint,self.SetPoint)
        # plt.xlim (0.0,max(self.Xaxis)+1)
        # plt.ylim (min(self.Yaxis)-10.0,max(self.Yaxis)+20.0)
        plt.xlim (0.0, 21.0)
        plt.ylim (140.0, 210.0)

        plt.xlabel('S')
        plt.ylabel("mm")
        plt.savefig('Object.png')


 


    def Autotune_update_object (self):
        
        qpimap = QPixmap('Object.png')
        self.ui.LB_image_PID_Autotune.setPixmap(qpimap)
        if self.Kp_motor != 0.0 and self.Ki_motor !=0.0 and self.Kp_motor != 0.0 :
            self.ui.OB_Kp1.setValue (self.Kp_motor)
            self.ui.OB_Ki1.setValue (self.Ki_motor)
            self.ui.OB_Kd1.setValue (self.Kd_motor)
            self.ui.ST1.setText ('Settling time (s) ='+ str(self.ST_motor))
            self.ui.OV1.setText ('Over shoot (%) ='+ str(self.OV_motor))
            self.ui.SSE1.setText ('Steady-state error (%) ='+ str(self.SSE_motor))

    def Advanced_Autotune_update_object (self):
        
        qpimap = QPixmap('Object.png')
        self.ui.LB_image_PID_Ad_autotune.setPixmap(qpimap)
        if self.Kp_motor != 0.0 and self.Ki_motor !=0.0 and self.Kp_motor != 0.0 :
            self.ui.OB_Kp2.setValue (self.Kp_motor)
            self.ui.OB_Ki2.setValue (self.Ki_motor)
            self.ui.OB_Kd2.setValue (self.Kd_motor)
            self.ui.ST_2.setText ('Settling time (s) ='+ str(self.ST_motor))
            self.ui.OS_2.setText ('Over shoot (%) ='+ str(self.OV_motor))
            self.ui.SSE_2.setText ('Steady-state error (%) ='+ str(self.SSE_motor))            

    def ObjectLastID (self):
        file_object1 = open ("Motor.csv", mode = "r", encoding= "utf-8-sig")
        # header = file_object1.readline ()
        row = file_object1.readline () 
        self.lastIDMotor = 0
        while row != "":
            self.lastIDMotor = self.lastIDMotor + 1
            row = file_object1.readline ()

        file_object1.close()
    
    def my_function(self,counter):
        dataDevice = counter
        sencond_time = 0
        previous_ST = 0.0
        index = self.sender().index
        PID_Para = dataDevice["PID"]
        Time = dataDevice ["time"]
        Quality = dataDevice["quality"]
        parameterPID = dataDevice["parameterPID"]
        self.Kp_motor = float(PID_Para ["kp"])
        self.Ki_motor = float(PID_Para["ki"])
        self.Kd_motor = float(PID_Para ["kd"])
        self.OV_motor = float(Quality["overshoot"])
        self.ST_motor = float(Quality["settlingTime"])
        self.SSE_motor = float(Quality["steadyStateError"])
        self.SP_motor = float (parameterPID["sp"])
        self.PV_motor = float (parameterPID["pv"])
        self.CV_motor = float (parameterPID["cv"])
        self.Day_motor = str(Time ["day"])
        self.Time_motor = str(Time ["time"])
        # print (dataDevice)
        # 24/11
        
        if self.ZN_mode:
                dataApp = self.cloud.receiveData(table="App", id=1)
                self.status = dataApp ["control"]["status"]
                print ("_________Status:", self.status)
                if (self.status == 'ZNDone' and self.BitSaveData == False):
                    
                    self.ZNDone()
                    self.ZN_mode = False
                if (self.status == 'ZNBegin'and self.one == False):
                    list_data = '0,0,0,0,0,0,0,0,0,0,0,0,0\n'
                    csvfile = open('Motor.csv',mode= 'a')
                    csvfile.write (list_data)
                    csvfile.close ()
                    self.one = True




        if index==1:         
            
            if ((self.PV_motor != self.ui.PV_OB1.value() or self.CV_motor != self.ui.CV_OB1.value() or self.SP_motor != self.ui.SV_OB1.value()) and (self.Previous_Time != self.Time_motor)) or (self.SSE_motor != self.ui.SSE_OB1.value()) :
                # print ('__________UPDATE___________')
                self.BitSaveData = True
                self.Previous_Time = self.Time_motor
                self.ui.PV_OB1.display(self.PV_motor) 
                self.ui.CV_OB1.display (self.CV_motor)
                self.ui.SV_OB1.display(self.SP_motor)
                self.ui.SL_OB1.display(self.ST_motor)
                self.ui.OS_OB1.display(self.OV_motor)    
                self.ui.SSE_OB1.display(self.SSE_motor) 

 
                print ('________SAVE___________')
                # print (dataDevice)

                self.lastPosition = 0.0
                list_data = str(self.lastIDMotor)+','+str(self.Kp_motor) +','+str(self.Ki_motor)+','+str(self.Kd_motor) +','+str(self.SP_motor)+','+str(self.PV_motor)+','+str(self.CV_motor)+','+str(self.OV_motor)+','+str(self.ST_motor)+','+str(self.SSE_motor)+','+str(self.Day_motor)+','+str(self.Time_motor)+'\n'
                csvfile = open('Motor.csv',mode= 'a')
                print (list_data)
                if list_data != 0:
                    csvfile.write (list_data)
                    self.lastIDMotor = self.lastIDMotor + 1
                    csvfile.close ()
                
                if ((float(self.Time_motor) == 20) and previous_ST != self.ST_motor ):
                    sencond_time = True
                else :
                    sencond_time = False   

                # 23/11
                self.SetPoint1_value = self.SP_motor
                previous_ST = self.ST_motor
            else:
                self.BitSaveData = False

            if (self.ui.MST_OB1.value() !=0.0 and self.ui.MOS_OB1.value() !=0.0 and self.ui.MSSE_OB1.value()!= 0.0):
                if (float(self.ui.MST_OB1.value()) <= self.ST_motor or float(self.ui.MOS_OB1.value()) <= self.OV_motor or float(self.ui.MSSE_OB1.value()) <= self.SSE_motor):
                    self.ui.OB1.setStyleSheet("background-color: rgb(245, 155, 66);")
                else:
                    self.ui.OB1.setStyleSheet("background-color: rgb(170, 255, 127);")
        
        if self.ML_mode == True:
            dataApp = self.cloud.receiveData(table="App", id=1)
            self.status = dataApp ["control"]["status"]
            print ('____MLStatus:',self.status )
            if (self.status == 'Done' and sencond_time == True ):
                print ('____MLDone____')
                self.ZNDone()
                self.ML_mode = False


    def ZNDone (self):
        file_object1 = open ("Motor.csv", mode = "r", encoding= "utf-8-sig")
        header = file_object1.readline ()
        row = file_object1.readline () 
        lastIDMotor = 0      
        x=[]
        y=[]
        x1=[]
        y1=[]
        x2=[]
        y2=[]
        x3=[]
        y3=[]
        x4=[]
        y4=[]
        SP1 = [200,200]
        SP2 = [150,150]
        Time = [0,20]
        curent_setpoint =0.0
        previous_setpoint =0.0

        current_Kp = 0.0
        current_Ki = 0.0
        current_Kd = 0.0
        current_OV = 0.0
        current_ST = 0.0
        current_SSE = 0.0

        ZN_Kp_list = [0,0,0,0,0]
        ZN_Ki_list =[0,0,0,0,0]
        ZN_Kd_list = [0,0,0,0,0]
        ZN_ST_list =[0,0,0,0,0]
        ZN_OV_list =[0,0,0,0,0]
        ZN_SSE_list = [0,0,0,0,0]
        counter = 0
        while row != "":
            lastIDMotor = lastIDMotor + 1
            row_list = row.split (',')

            curent_setpoint = float (row_list[4])
            current_Kp = float (row_list[1])
            current_Ki = float (row_list[2])
            current_Kd = float (row_list[3])
            current_OV = float (row_list[7])
            current_ST = float (row_list[8])
            current_SSE = float (row_list[9])
            ZN_OV_list[0] = current_OV
            ZN_ST_list[0] = current_ST
            ZN_SSE_list[0] = current_SSE

            # print (curent_setpoint)
            if (curent_setpoint == previous_setpoint):

                # print ("giong")
                x.append(float(row_list[11]))
                y.append (float(row_list[6]))

                ZN_Kp_list[0] = current_Kp
                ZN_Ki_list[0] = current_Ki
                ZN_Kd_list[0] = current_Kd

            if (curent_setpoint != previous_setpoint):
                # print ("_____khac______")
                if (counter == 0):
                    x1 =x 
                    y1 =y
                    x = []
                    y = []

                    ZN_Kp_list[1] = ZN_Kp_list [0]
                    ZN_Ki_list[1] = ZN_Ki_list [0]
                    ZN_Kd_list[1] = ZN_Kd_list [0]

                    ZN_OV_list[1] = ZN_OV_list[0]
                    ZN_ST_list[1] = ZN_ST_list[0]
                    ZN_SSE_list[1] = ZN_SSE_list[0]

                    counter = 1
                    # print ('?????????????Counter=1??????????????')
                if (counter == 1):
                    x2= x1
                    y2 = y1
                    x1 =x
                    y1 =y
                    x = []
                    y = []

                    ZN_Kp_list[2] = ZN_Kp_list [1]
                    ZN_Ki_list[2] = ZN_Ki_list [1]
                    ZN_Kd_list[2] = ZN_Kd_list [1]

                    ZN_Kp_list[1] = ZN_Kp_list [0]
                    ZN_Ki_list[1] = ZN_Ki_list [0]
                    ZN_Kd_list[1] = ZN_Kd_list [0]
            
                    ZN_OV_list[2] = ZN_OV_list[1]
                    ZN_ST_list[2] = ZN_ST_list[1]
                    ZN_SSE_list[2] = ZN_SSE_list[1]

                    ZN_OV_list[1] = ZN_OV_list[0]
                    ZN_ST_list[1] = ZN_ST_list[0]
                    ZN_SSE_list[1] = ZN_SSE_list[0]

                    counter = 2
                    # print ('?????????????Counter=2??????????????')
                if (counter == 2):
                    x3 = x2
                    y3 = y2
                    x2= x1
                    y2 = y1
                    x1 =x
                    y1 =y
                    x = []
                    y = []

                    ZN_Kp_list[3] = ZN_Kp_list [2]
                    ZN_Ki_list[3] = ZN_Ki_list [2]
                    ZN_Kd_list[3] = ZN_Kd_list [2]

                    ZN_Kp_list[2] = ZN_Kp_list [1]
                    ZN_Ki_list[2] = ZN_Ki_list [1]
                    ZN_Kd_list[2] = ZN_Kd_list [1]

                    ZN_Kp_list[1] = ZN_Kp_list [0]
                    ZN_Ki_list[1] = ZN_Ki_list [0]
                    ZN_Kd_list[1] = ZN_Kd_list [0]

                    ZN_OV_list[3] = ZN_OV_list[2]
                    ZN_ST_list[3] = ZN_ST_list[2]
                    ZN_SSE_list[3] = ZN_SSE_list[2]

                    ZN_OV_list[2] = ZN_OV_list[1]
                    ZN_ST_list[2] = ZN_ST_list[1]
                    ZN_SSE_list[2] = ZN_SSE_list[1]

                    ZN_OV_list[1] = ZN_OV_list[0]
                    ZN_ST_list[1] = ZN_ST_list[0]
                    ZN_SSE_list[1] = ZN_SSE_list[0]

                    counter = 3
                    # print ('?????????????Counter=3??????????????')
                if (counter == 3):
                    x4=x3
                    y4=y3
                    x3 = x2
                    y3 = y2
                    x2= x1
                    y2 = y1
                    x1 =x
                    y1 =y
                    x = []
                    y = []

                    ZN_Kp_list[4] = ZN_Kp_list [3]
                    ZN_Ki_list[4] = ZN_Ki_list [3]
                    ZN_Kd_list[4] = ZN_Kd_list [3]

                    ZN_Kp_list[3] = ZN_Kp_list [2]
                    ZN_Ki_list[3] = ZN_Ki_list [2]
                    ZN_Kd_list[3] = ZN_Kd_list [2]

                    ZN_Kp_list[2] = ZN_Kp_list [1]
                    ZN_Ki_list[2] = ZN_Ki_list [1]
                    ZN_Kd_list[2] = ZN_Kd_list [1]

                    ZN_Kp_list[1] = ZN_Kp_list [0]
                    ZN_Ki_list[1] = ZN_Ki_list [0]
                    ZN_Kd_list[1] = ZN_Kd_list [0]

                    ZN_OV_list[4] = ZN_OV_list[3]
                    ZN_ST_list[4] = ZN_ST_list[3]
                    ZN_SSE_list[4] = ZN_SSE_list[3]

                    ZN_OV_list[3] = ZN_OV_list[2]
                    ZN_ST_list[3] = ZN_ST_list[2]
                    ZN_SSE_list[3] = ZN_SSE_list[2]

                    ZN_OV_list[2] = ZN_OV_list[1]
                    ZN_ST_list[2] = ZN_ST_list[1]
                    ZN_SSE_list[2] = ZN_SSE_list[1]

                    ZN_OV_list[1] = ZN_OV_list[0]
                    ZN_ST_list[1] = ZN_ST_list[0]
                    ZN_SSE_list[1] = ZN_SSE_list[0]
                    
            previous_setpoint = curent_setpoint
            row = file_object1.readline ()
        print ('____X4____:',x4)
        print ('____Y4____:',y4)    
        print ('____X3____:',x3)
        print ('____Y3____:',y3)
        print ('____X2____:',x2)
        print ('____Y2____:',y2)
        print ('____X1____:',x1)
        print ('____Y1____:',y1)
        print ('____X0____:',x)
        print ('____Y0____:',y)

        print ('____Xaxis____:',self.Xaxis)
        print ('____Yaxis____:',self.Yaxis)

        print ('___________Kp:',ZN_Kp_list)
        print ('___________Ki:',ZN_Ki_list)
        print ('___________Kd:',ZN_Kd_list)

        print ('___________OV:',ZN_OV_list)
        print ('___________ST:',ZN_ST_list)
        print ('___________SSE:',ZN_SSE_list)

        # ////////////////////Luu cac gia tri chat luong

        self.ZN_Kp_list = ZN_Kp_list
        self.ZN_Ki_list = ZN_Ki_list
        self.ZN_Kd_list = ZN_Kd_list
        self.ZN_OV_list = ZN_OV_list
        self.ZN_ST_list = ZN_ST_list
        self.ZN_SSE_list = ZN_SSE_list
        if (self.ZN_mode):
        # ////////////////////Object___vs___Classic
            plt.cla()
            plt.plot (x3,y3)
            plt.plot (Time,SP1)
            plt.plot (self.Xaxis,self.Yaxis)
            plt.plot (Time,SP2)
            plt.xlim (0.0, 21.0)
            plt.ylim (140.0, 210.0)
            plt.xlabel('S')
            plt.ylabel("mm")
            plt.savefig ('Classic_PID.png')

            ## ////////////////////Object___vs___PessenIntergration
            plt.cla()
            plt.plot (x2,y2)
            plt.plot (Time,SP1)
            plt.plot (self.Xaxis,self.Yaxis)
            plt.plot (Time,SP2)
            plt.xlim (0.0, 21.0)
            plt.ylim (140.0, 210.0)
            plt.xlabel('S')
            plt.ylabel("mm")
            plt.savefig ('PI_PID.png')

            ## ////////////////////Object___vs___SomeOvershoot
            plt.cla()
            plt.plot (x1,y1)
            plt.plot (Time,SP1)
            plt.plot (self.Xaxis,self.Yaxis)
            plt.plot (Time,SP2)
            plt.xlim (0.0, 21.0)
            plt.ylim (140.0, 210.0)
            plt.xlabel('S')
            plt.ylabel("mm")
            plt.savefig ('SO_PID.png')
            ## ////////////////////Object___vs___SomeOvershoot
            plt.cla()
            plt.plot (x,y)
            plt.plot (Time,SP1)
            plt.plot (self.Xaxis,self.Yaxis)
            plt.plot (Time,SP2)
            plt.xlim (0.0, 21.0)
            plt.ylim (140.0, 210.0)
            plt.xlabel('S')
            plt.ylabel("mm")
            plt.savefig ('NO_PID.png')

        if (self.ML_mode):
            ## ////////////////////Object___vs___AfterML
            plt.cla()
            plt.plot (x,y)
            plt.plot (Time,SP1)
            plt.plot (self.Xaxis,self.Yaxis)
            plt.plot (Time,SP2)
            plt.xlim (0.0, 21.0)
            plt.ylim (140.0, 210.0)
            plt.xlabel('S')
            plt.ylabel("mm")
            plt.savefig ('ML_PID.png')


class ThreadClass(QtCore.QThread):
    
    any_signal = QtCore.pyqtSignal(dict)
    def __init__(self, parent=None,index=0):
        super(ThreadClass, self).__init__(parent)
        self.index=index
        self.cloud = cloudAWS()
        self.ui = Ui_MainWindow()
        self.is_running = True

    def run(self):
        while True:
            try:

                dataDevice = self.cloud.receiveData(table="Device", id=1)
                
            except:
                print("Receive from table Device Error")
            # time.sleep (0.1)
            self.any_signal.emit(dataDevice)
    def stop(self):
        self.is_running = False
        print('Stopping thread...',self.index)
        self.terminate()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyApp()
    w.show()
    sys.exit(app.exec_()) 