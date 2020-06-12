import time
from datetime import datetime
from scapy.all import *
from socket import *
from time import sleep

#Furkan Soysal -------------160401017

localTime=datetime.now()    
utcTime=datetime.utcnow()
utcVariable="+0"

#zamanın UTC farkının hesaplanması
def UTCType():
    differenceHour=localTime.hour-utcTime.hour
    if differenceHour >= 0:
        return "UTC+"+str(differenceHour)
    else:
        return "UTC"+str(differenceHour)
        
#yukarıda verilen utcVariable değeri hesaplanması
def setUTC(changedUTC:str):
    
    localTime=datetime.now()
    
    listUTC=list(changedUTC)
    # print(listUTC)
    if listUTC[0]=="+":
        hour1=localTime.hour+int(listUTC[1])
    elif listUTC[0]=="-":
        hour1=localTime.hour-int(listUTC[1])
    else:
        print("Lütfen + veya - giriniz.")
    hour1=hour1%24
    localTime= localTime.replace(hour=hour1)
    # print(localTime)
    return localTime

localTime=setUTC(utcVariable)

# print(UTCType())

_host = gethostname()
_port=142

server_socket = socket(AF_INET,SOCK_STREAM)
server_socket.bind((_host, _port))
server_socket.listen(1)


while True:
    conn, address = server_socket.accept()
    
    print("\nBağlanılan Host: " + str(address))
    gecikme=datetime.now().timestamp()#gönderilen zaman
    
    
    conn.send(str(gecikme).encode())
    
    gecikme=datetime.now().timestamp()-float(conn.recv(1024))# gecikme ile gönderilen zamanın şimdiki zamandan farkı alınıyor
    # print(gecikme)
    millis=(datetime.now().timestamp()+gecikme)*1000 # zaman milisaniyeye çevriliyor
    conn.send(str(millis).encode())# milisaniye gönderimi
    sleep(0.0008)
    conn.send(str(UTCType()).encode())# UTC ve offsetinin gönderimi

    

