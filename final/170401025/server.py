import socket
import ntplib
import time
import os
import sys
import datetime
import pickle

#170401025 / Eda Defterli

soket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host="localhost"
port=142
soket.bind((host,port))
print("%s:%d server baslatildi."%(host,port))
print("Kullanici bekleniyor.")
soket.listen(5)
baglanti,adres=soket.accept()
print("Bir baglanti kabul edildi.",adres)
mesaj="Sunucu tarafi basarili"
mesaj1=mesaj.encode('utf-8')
baglanti.sendto(mesaj1,(host,port))
data=baglanti.recv(1024)
print(data)

date_time = datetime.datetime.now()
time = date_time.time()
zmn=str((time.hour*3600000)+(time.minute)*60000+(time.second)*1000+(time.microsecond)/1000) #zamani milisaniyeye cevirir.
zmn1=zmn.encode('utf-8')
baglanti.sendto(zmn1,(host,port))

greenwich=datetime.datetime.utcnow()
zaman=datetime.datetime.now()
baslangic=[zaman.hour,zaman.minute,zaman.second,zaman.microsecond]
utc=zaman.hour-greenwich.hour
if(utc>=0):
    utc="UTC+" + str(utc)
else:
    utc="UTC" + str(utc)
print(zmn1,utc)

soket.listen(5)
connection, client_address = soket.accept()
simdizaman=datetime.datetime.now()
zamanliste=[simdizaman,utc]
eleman=pickle.dumps(zamanliste)
connection.send(eleman)
soket.close()