#Arzu Tepe 170401008

import socket
import os 
from time import gmtime, strftime
import time 
import datetime

client=socket.socket() 
host='192.168.0.103'
port = 142
komut = 'sudo date --set='
client.connect((host,port))
print("Bağlantı yapıldı")
mesaj=client.recv(1024) 
print(mesaj.decode())
client.sendto("merhaba ".encode(), (host, port))
mesaj=client.recv(1024) #bu mesaj ile zaman bilgisi alındı
a = mesaj.decode().split(" ")
#bu kısımda mesajı alıp tarih formuna cevirdik
mesaj = a[0]
print(mesaj)
s = float(mesaj) / 1000.0
saat = datetime.datetime.fromtimestamp(s).strftime('%m/%d/%Y %H:%M:%S.%f')
print(saat)
komut = komut + '"' + saat + '"'
print(komut, 'komut')
os.system(komut)
client.close() 
