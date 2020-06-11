#Eda ARSLAN 170401024

import socket
import os
from time import gmtime,strftime
from datetime import datetime
import time
import datetime

#host = input("Sunucu ip adresini girin: ")

host = '192.168.1.36'
port = 142
msg = "gecikme hesabi"

kmt = 'sudo date --set='

frmt = '%m/%d/%Y %H:%M:%S.%f'

try:
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host,port))
    print("Sunucu ile bağlanılıyor.")
    
except s.error:
    print("Hata!",s.error)
    sock.close()

msj=s.recv(1024)


offset=s.recv(1024)
offset=offset.decode()
##print(offset)

data=s.recv(1024)
data=data.decode()
print("data: ",data)

print(str(data)+' UTC'+str(offset))

##tarih=s.recv(1024) 
##tarih=tarih.decode()
##print("tarihg: ",tarih) 

a = float(data)/1000.0 

##print("a: ",a)

saat = datetime.datetime.fromtimestamp(a).strftime(frmt)
print("Tarih ve Saat: ",saat)

kmt = kmt + '"' + saat + '"'
print(kmt, 'komut')
os.system(kmt)

s.close()
