#Eda ARSLAN 170401024

import socket
from datetime import datetime
import time

#host = input("Sunucu ip adresini girin: ")
host='192.168.1.36'
port = 142

offset='0'


ms = int(round(time.time() * 1000))
##print(ms)

msg = str(ms)

##frmt = "%Y-%m-%d %H:%M:%S%f %Z%z"
    
##def kontrol(milisaniye):
##    year=time.gmtime(milisaniye/1000).tm_year
##    month=time.gmtime(milisaniye/1000).tm_mon
##    day=time.gmtime(milisaniye/1000).tm_mday
##    hour=time.gmtime(milisaniye/1000).tm_hour
##    minute=time.gmtime(milisaniye/1000).tm_min
##    sec=time.gmtime(milisaniye/1000).tm_sec
##    msec=milisaniye%1000
##    tarih=(int(year),int(month),int(day),int(hour),int(minute),int(sec),int(msec))
##    return tarih 
    
def degis():
    zaman = datetime.now()
##    print("z: ",zaman)
    a = int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds() * 1000)
    z = int(offset) - 3
    a = a + 3600000*z
##    print("a: ",a)
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
##            print("gecikme önce: ",date)
            date=date+gecikme
##            print("d: ",date)
            data.send(str(date).encode())
##            date=kontrol(date)
##            print("date: ",date)
##            data.send(str(date).encode())
            break
        else:
            data.send(str(offset).encode())
            msj = gecikme_son+gecikme
            mesj=str(msj.timestamp()*1000)
##            print("a: ",msj)
            data.send(str(mesj).encode())
##            print("msj: ",msj)
##            data.send(str(msj).encode())
##            print("gecikme son: ",gecikme_son)
            
            
            
            break
    data.close()

