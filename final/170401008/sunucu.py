#Arzu Tepe 170401008

import time
import socket
import datetime  
from time import gmtime, strftime


#1 saat 3600000 milisaniyedir  

server=socket.socket() 
host='192.168.0.103'
port = 142 
server.bind((host,port))
server.listen(1) 
print("Bağlantı bekleniyor...")
sunucu,bilgi=server.accept() 
print("Bir bağlantı kabul edildi")
start = time.time()
sunucu.sendto("Merhaba!!".encode(),(host,port) )
mesaj=sunucu.recv(1024)
finish = time.time()
fark = (finish - start)*1000
print(mesaj.decode())
print("geciken zaman: ",fark)


milisaniye = int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000) 

a = input("zaman dilimini değiştirmek için 1 e basın: ")
if(a == '1'):
    sa = input("zaman dilimi girin (utc+2 zaman değerinin sadece +2 değerini girmek yeterlidir): ")
    saa = int(sa) - 3    
    milisaniye = milisaniye + int(saa)*3600000    
    zaman = milisaniye + fark 
    zaman = str(milisaniye) + ' UTC' + str(sa)
    sunucu.sendall(str(zaman).encode('utf-8'))
    
else:
    zaman = milisaniye + fark 
    zaman = str(zaman) + ' UTC' + str(+3)
    print(zaman)
    sunucu.sendall(str(zaman).encode('utf-8')) 


server.close()
