import socket
import os
import sys
import datetime
import pickle
import time

#160401019
#Sena Günay

host = "127.0.0.1"
port = 142


greenwich=datetime.datetime.utcnow()
zaman=datetime.datetime.now()
ilk_zaman=[zaman.hour,zaman.minute,zaman.second,zaman.microsecond]
utc=zaman.hour-greenwich.hour

if(utc>=0):
    utc="UTC+" + str(utc)
else:
    utc="UTC" + str(utc)
print(zaman,utc)

try:
    sunucu = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #TCP kullanildigindan SOCK_STREAM
    sunucu.bind((host, port))
    print("socket {} portuna bağlandı".format(port))

except socket.error as hata:
    print("Hata:",hata)

# Client ile bağlantı kurulursa

sunucu.listen(5)
baglanti, addr = sunucu.accept()
print('Gelen bağlantı:', addr)
mesaj = ("Baglanti icin tesekkurler. Saatiniz degistirilirken lutfen bekleyin. ").encode('utf-8')
baglanti.sendto(mesaj,addr)

yenizaman=datetime.datetime.now()
zaman_son=[yenizaman,utc]
sonuc=pickle.dumps(zaman_son)
baglanti.send(sonuc)





