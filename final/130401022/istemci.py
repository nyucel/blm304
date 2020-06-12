import socket
import time
from datetime import datetime
import os,sys
import win32api

#HASAN SESLİ                    #Hasan SESLİ

def saatGuncelleWindows( millisecondsX):
    millisecondsX = millisecondsX + 2*1000
    #gecikme milisaniye olarak hesaplandı
    seconds=(millisecondsX/1000)%60
    seconds = int(seconds)
    minutes=(millisecondsX/(1000*60))%60
    minutes = int(minutes)
    hours=(millisecondsX/(1000*60*60))%24
    hours=int(hours)

    yıl = int(datetime.now().strftime("%Y")) 
    ay = int(datetime.now().strftime("%m"))
    gün = int(datetime.now().strftime("%d"))
    #gecikme hesaplama 1024 kb verinin yanıt olarak karşıdan gelmesi yaklaşık 1sn
    #artı ek olarak 1sn fonksiyonların çalışması toplam = 2 sn
    win32api.SetSystemTime(yıl,ay,7,gün,hours,minutes,seconds,600)
    print("\n",datetime.fromtimestamp(millisecondsX/1000))

def saatGuncelleLinux(millisecondsX):
    millisecondsX = millisecondsX + 2*1000  #2 saniye
    #gecikme milisaniye olarak hesaplandı
    linux_tarih_komut = datetime.fromtimestamp(millisecondsX/1000)
    os.system("sudo date --s  '%s'" % linux_tarih_komut)
    print("Saat : ",linux_tarih_komut)


IP = '127.0.0.1'
TCP_PORT = 142
BUFFER_BOYUTU = 1024

MESSAGE = "b'Hey sunucu, saat kac?"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, TCP_PORT))
s.send(MESSAGE.encode('utf8'))

data = s.recv(BUFFER_BOYUTU)
mesaj= data.decode('utf8')
saat_bilgisi = mesaj.split(" ")
print("\nGelen yanıt : "+saat_bilgisi[0]+"  "+saat_bilgisi[1])

milliseconds = saat_bilgisi[0]
milliseconds=int(milliseconds)

if (sys.platform == 'win32'):
    saatGuncelleWindows(milliseconds)
elif(sys.platform == 'linux2' or sys.platform == 'linux'):
    saatGuncelleLinux(milliseconds)


s.close()
print('yeni saat ayarlandi..\n')
print("baglanti sonlandi..\n")
