#Arife Oran - 160401071

import socket
from time import gmtime, strftime
import time
import datetime
import os

IP='192.168.1.106'
Port = 142
cmd = 'sudo date --set='

clientSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((IP,Port))

msg=clientSocket.recv(1024)
print(msg.decode())

getTime=clientSocket.recv(1024) #Sunucudan zaman bilgisi alındı
time_start = time.time()
serverTime, utc = getTime.decode().split("-UTC")
print("Milisaniye cinsinden sunucunun saati: ", serverTime)
s_Time = float(serverTime) / 1000.0
delayTime = time.time() - time_start
newTime = s_Time + delayTime  #Gecikme hesaplanıyor

print("Gecikme zamanı: ", delayTime)
serverDateTime = datetime.datetime.fromtimestamp(newTime).strftime('%m/%d/%Y %H:%M:%S.%f')
print("Bilgisayarın saati ayarlanıyor..")
cmd = cmd + '"' + serverDateTime + '"'
print(serverDateTime)
os.system(cmd)

clientSocket.close()
