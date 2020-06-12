#170401022 Cihan PAR
import socket
import os 
import time
Target_IP= "192.168.2.8"
TCP_Port= 142
print("Forwardaing to targeted IP addresses..")
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
TCP_Link = (Target_IP,TCP_Port)
Message1 = "Time information "
try:
    sock.connect(TCP_Link)
except:
    print("Connection error")
    sock.close
    exit()
print("connection accepted")
timer = sock.recv(1024)
print("received time = "+timer.decode())
timer = timer.decode().split(",")
Message = "Time data has received."
sock.send(Message.encode())
time_ms = float(timer[0])/1000
time_zone = timer[1]
delay_time = sock.recv(1024)
print(delay_time.decode()+"ms")
time_ms = time_ms - float(delay_time.decode())/1000
settime = time.ctime(time_ms)
print(settime,time_zone,"\n")
set_time_command = 'sudo date --set='
set_time_command = set_time_command + '"' + settime +'"'
os.system(set_time_command)
Message = "Time data has received and system time has been set succesfully."
sock.send(Message.encode())