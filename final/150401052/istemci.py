#Erdin ALHAS 150401052

import socket, os, time, sys
from os import system, name
from datetime import datetime, timedelta

SIZE = 2048
port = 142
ip = input("Sunucu ip adresi giriniz: ")
i_soket = socket.socket()
i_soket.connect((ip, port))
print("Sunucu ile istemci arasinda baglanti kuruldu.")

remoteTime = i_soket.recv(SIZE)  
i_soket.send(bytes("tamam", encoding='utf-8'))  
print("\nIstemci Zamani: " + str(datetime.now().strftime("%d %B %Y %H:%M:%S.%f ")) + "UTC +3")

simdikiZaman = i_soket.recv(SIZE)
zamanDilimi = i_soket.recv(SIZE)
print("\nSunucu Zamani: " + simdikiZaman.decode("utf-8") + zamanDilimi.decode("utf-8"))

tarih = simdikiZaman.decode().split(" ")
tarih = tarih[0] + " " + tarih[1] + " " + " " + tarih[2] + " " + tarih[3] + " "

os.system('date --set "%s" +\"%%d %%B %%Y %%H:%%M:%%S.%%6N\"' % tarih)
os.system("sudo hwclock -w")
print("\n>> Sistem zamani guncellendi.\n")