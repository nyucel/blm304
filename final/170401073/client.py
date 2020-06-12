#Mehmet Salih Çelik 170401073
import socket
import datetime
import os
import time
import sys


ipiste=str(input("Sunucunun ip adresini giriniz :"))
HOST = ipiste
PORT = 142

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    a=time.time()
    data = s.recv(1024)
    b=time.time()
    data=data.decode("utf-8")


def utchesapla():
    x = datetime.datetime.now()
    y = str(x.astimezone().timetz())
    z = y.strip()[15:18]
    if z[1]=="0":
        z=int(z[0]+z[2])
    else:
        z=int(z[0]+z[1]+z[2])
    return z

z=int(utchesapla())
x=float(data.split()[0])/1000
y=int(data.split()[2])-z
t=y*3600
x=x+t
gecikme=b-a
gecikmelizaman=x+(gecikme)
ayarla=datetime.datetime.fromtimestamp(x)
ayarla=str(ayarla)
ayarla2=datetime.datetime.fromtimestamp(gecikmelizaman)
ayarla2=str(ayarla2)
print("Sunucudan alinan zaman verisi (ms): ",data.split()[0])
print("Alinan verinin tarihe cevrilmisi :",ayarla)
print("Veri alisverisinde yasanan gecikme ",gecikme," saniye")
print("Gecikme eklenerek hesaplanan zaman : ",datetime.datetime.fromtimestamp(gecikmelizaman))
komut="sudo date -s "+'"'+ayarla2+'"'
komut2="timedatectl set-ntp false"
komut3="sudo hwclock -w"
os.system(komut)
os.system(komut2)
os.system(komut3)

print("Client saati ",ayarla2," olarak guncellendi")


