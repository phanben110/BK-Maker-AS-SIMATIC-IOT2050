import csv
import matplotlib.pyplot as plt


file = open("Motor.csv", mode = "r", encoding= "utf-8-sig")
header = file.readline () 
lastIDMotor = 0
lastSetPoint = 0
row = file.readline ()
while row != "":
    lastIDMotor = lastIDMotor + 1
    row_list = row.split(",")
    lastSetPoint = row_list[4]
    row = file.readline ()
print (lastIDMotor)   
print (lastSetPoint)
file.close()

file = open("Motor.csv", mode = "r", encoding= "utf-8-sig")
header = file.readline () 

row2 = file.readline ()
CV1 = []
Time_CV1 =[]
while row2 !="":
    row_list2 = row2.split(",")
    currentSetPoint = row_list2 [4]
    if currentSetPoint == lastSetPoint :
        CV1.append (float(row_list2[6]))
        Time_CV1.append (float(row_list2[11]))
    else :
        CV1 =[]
        Time_CV1 =[]
    row2 = file.readline () 
print (CV1)
print (Time_CV1)
file.close()

Setpoint = [float(lastSetPoint),float(lastSetPoint)]
TimeSetPoint = [min(Time_CV1),max(Time_CV1)]
plt.plot (Time_CV1,CV1)
plt.plot (TimeSetPoint,Setpoint)
plt.xlim (0.0,max(Time_CV1)+1)
plt.ylim (min(CV1),max(CV1)+20.0)
plt.xlabel('S')
plt.ylabel("mm")
plt.savefig('aaa.png')

plt.show()


