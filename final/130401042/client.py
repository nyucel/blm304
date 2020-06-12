import socket
import time
from datetime import datetime
import win32api
import os,sys

#BAHAR ÇİFTÇİ               
PORT = 142
BUFFER = 1024
ilk_mesaj = "b' Saat kaç?"
istemci = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def saatAyarla(milisaniye , x):
    if(x == 1):
        saniye=(milisaniye/1000)%60
        saniye = int(saniye)
        dakika=(milisaniye/(1000*60))%60
        dakika = int(dakika)
        saat=(milisaniye/(1000*60*60))%24
        saat=int(saat)
        milli=900
        win32api.SetSystemTime(int(datetime.now().strftime("%Y")),int(datetime.now().strftime("%m")),7,int(datetime.now().strftime("%d")),saat,dakika,saniye,milli)
        print("Saat ayarlandi.. kontrol ediniz\n")
    if(x == 2):
        linux = datetime.fromtimestamp(milisaniye/1000)
        os.system("sudo date --s  '%s'" % linux)


while True:
    IP = input("Sunucu ip adresini girin :  ")
    if(IP == "127.0.0.1"):
        istemci.connect((IP,PORT))
        istemci.send(ilk_mesaj.encode())
        baslangic = int(round(time.time() * 1000))
        print("\nSunucu ile baglantı kuruldu..\n")
        veri = istemci.recv(BUFFER)
        gelenCevap = veri.decode()
        gelenCevap = gelenCevap.split(" ")
        print("b' Yanıt :  ",gelenCevap[0],"  ",gelenCevap[1])
        yanit = gelenCevap[0]
        yanit = int(float(yanit))
        bitis = int(round(time.time() * 1000))
        gecikme_suresi = bitis - baslangic
        gecikmeli_zaman = yanit + gecikme_suresi #gecikme süresi hesaplanıyor
        if(sys.platform == "win32"):
            saatAyarla(gecikmeli_zaman,1)
            break
        elif(sys.platform == "linux2" or sys.platform == "linux"):
            saatAyarla(gecikmeli_zaman,2)
            break
        
    else:
        print("yanlis ip girdiniz tekrar deneyin.. \n")

istemci.close()
print("\nSunucu baglantiyi sonlandirdi")
