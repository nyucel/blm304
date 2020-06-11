#Eda ARSLAN 170401024

import socket
from datetime import datetime
import time

host = input("Sunucu ip adresini girin: ")
#host='192.168.1.36'
port = 142

offset='0'


ms = int(round(time.time() * 1000))

msg = str(ms)

def degis():
    zaman = datetime.now()
    a = int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds() * 1000)
    z = int(offset) - 3
    a = a + 3600000*z
    return a

try:
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((host,port))
    print("Socket oluşturuldu.")
    s.listen(1)
except s.error:
    print("Hata!",s.error)
    
while(True):
    data,adr = s.accept()
    while(True):
        gecikme_bas = datetime.now()
        data.send(msg.encode())
        gecikme_son = datetime.now()
        gecikme = (gecikme_son - gecikme_bas)/2
        print("Gecikme: ",gecikme)
        if(offset!='0'):
            data.send(str(offset).encode())
            date=degis()
            gecikme=gecikme.total_seconds()*1000
            date=date+gecikme
            data.send(str(date).encode())
            break
        else:
            data.send(str(offset).encode())
            msj = gecikme_son+gecikme
            mesj=str(msj.timestamp()*1000)
            data.send(str(mesj).encode())
            
            
            
            break
    data.close()

