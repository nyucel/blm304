# 170401018 -- Cemre UZUN

from os import system, name
import os, sys
from datetime import datetime
import socket


def ekraniTemizle():
    if(name == 'nt'):
        _ = system('cls')
    else:
        _ = system('clear')

#---  -------------------------------- ISTEMCI --------------------------------  ---#

IP = '10.0.2.15'
PORT = 142

try:
    istemciS = socket.socket()
except:
    ekraniTemizle()
    print("\n-> HATA!\nIstemci olusturulamadi islemleri tekrarlayiniz..")
    sys.exit()
print("\n...Istemci Olusturuldu... *** ")
print ("\n...Istemci Baglaniyor...\n...Sunucu calismaya basliyor...")

try:
    istemciS.connect((IP, PORT))
except:
    ekraniTemizle()
    print("\n-> HATA!\nSunucu bulunamadi. Sunucunun calisiyor oldugundan emin olunuz..")
    sys.exit()

print("\n...Sunucu ile istemci arasinda baglanti kuruldu...")
print("\n.....................................................")

kontrolZaman = istemciS.recv(3072) #Veriyi yakalamak icin recv kullanildi.
print ("\n...Gecikme kontrolu yapiliyor...")
istemciS.send(bytes("kontrolluIslem", encoding='utf-8'))
print ("\n...Gecikme suresi hesaplandi...")

print("\n-> Istemci Zamani: " + str(datetime.now()) + " UTC +3")

yeniSaat = istemciS.recv(2048)

zamanDilimi = istemciS.recv(2048)
print("\n-> Sunucudan gelen zaman: " + yeniSaat.decode("utf-8") + " " + zamanDilimi.decode("utf-8"))
print ("\n...Istemci Kapatildi...") 

komut = 'date --set "%s" +\"%%A %%d %%B %%Y %%H:%%M:%%S.%%6N\"' #Yeni zaman ekrana yazıldı
os.system(komut % yeniSaat.decode("utf-8"))
os.system("sudo hwclock -w")

print("\n...Sistem saati ayarlandi...")
