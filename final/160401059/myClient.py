import socket                
import os
import datetime as dt
#Berat Kanar - 160401059


#2020-6-10 11:42:23 -->Date Format

os.system('timedatectl set-time="19:23:00.097" ')
socket1 = socket.socket()  #Socket olusturduk     

host = "192.168.1.25" #Baglanılacak ip
port = 142               


command = 'timedatectl set-time='
socket1.connect((host, port)) 

    
rsp = socket1.recv(1024)
print(rsp.decode("utf-8"))
    
    
socket1.send(rsp)  #Zamanı kesin hesaplayabilmek için gecikme hesaplaması.
   
    
command = command + socket1.recv(1024).decode() + '"'
print(command)
    
utc = socket1.recv(1024)
print(utc.decode())
    
os.system(command)  #gelen komutu çalıştırdık.
socket1.close() 
    
    
