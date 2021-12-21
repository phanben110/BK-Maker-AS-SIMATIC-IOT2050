# Đầu vao hệ thống là Kp, Ki, Kd
# Tính ra Ku và Tu

Kp = 0.025999
Ki = 0.004194638
Kd = 0.01677855
Ku = Kp/0.6
Tu =1.2*Ku / Ki

print ('Ku,Tu:',Ku,Tu)

# Với luật Pessen Integration (PI)

Kp_PI = 0.7*Ku
Ki_PI = 1.75*Ku/Tu
Td_PI = 3*Tu/20
Kd_PI = Kp_PI/Td_PI
print ('LuatPI:',Kp_PI,Ki_PI,Kd_PI)

# Với luật Some Overshoot (SO)
# Kp_SO = Ku/3
# Ki_SO = (2/3)*Ku/Tu
# Kd_SO = (1/9)*Ku/Tu
# print ('LuatSO',Kp_SO,Ki_SO,Kd_SO)

Kp_SO = Ku/3
Ki_SO = (2/3)*Ku/Tu
Td_SO = Tu/3
Kd_SO = Kp_SO/Td_SO
print ('LuatSO',Kp_SO,Ki_SO,Kd_SO)

#Với luật No Overshoot (NO)

Kp_NO = 0.2*Ku
Ki_NO = (2/5)*Ku/Tu
Td_NO = Tu/3
Kd_NO = Kp_NO/Td_NO
print ('LuatNO:',Kp_NO,Ki_NO,Kd_NO)

# Đầu ra là 3 luật này cộng với thông số gốc nữa là 4