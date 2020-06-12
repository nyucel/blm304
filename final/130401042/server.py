import socket
import time
from datetime import datetime
import win32api
import os,sys
#YAZAN
#BAHAR ÇİFTÇİ
SUNUCU_IP = '127.0.0.1'
DINLENEN_PORT = 142
BUFFER = 1024
UTC_ZAMAN_DILIMI = "UTC-2"

sunucu = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sunucu.bind((SUNUCU_IP,DINLENEN_PORT))
sunucu.listen(1)

baglanti, adres = sunucu.accept()

print("Baglanan bilgisayar adresi :  ", adres)
gelen_veri = baglanti.recv(BUFFER)
print("---  ",gelen_veri.decode())

sunucu_utc = int( UTC_ZAMAN_DILIMI[3:] )
yerel_utc = int(time.strftime('%z'))/100 #degiskendeki 00 ları silmek için

print("Yanıt hepsine basarıyla gönderildi")

milisaniye = int(round(time.time() * 1000))
utc_zaman_farki = sunucu_utc - yerel_utc
zaman_farki = utc_zaman_farki*60*60*1000
milisaniye += zaman_farki

response = str(milisaniye) +" " + UTC_ZAMAN_DILIMI
baglanti.send(response.encode())
baglanti.close()
print("sunucu baglantiyi sonlandirdi")
