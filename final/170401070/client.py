#170401070-Başak KILIÇ

import socket 
import os
from os import sys
from datetime import datetime
import time

ip = input("Sunucunun ip adresi:  ")
port = 142

istemciSocket = socket.socket()
try:
	istemciSocket.connect((ip, port))			
except:
    print("Önce sunucu bağlantısı kurulmalı.\n")
    sys.exit()
    
print("Sunucu istemci baglantisi saglandi.")

sunucuZaman = istemciSocket.recv(2048)		#ntpserver'dan gönderilen zaman bilgisi yakalanır.
istemciSocket.send(bytes("true", encoding='utf-8'))

guncelZaman = istemciSocket.recv(2048)		
zamanDilimi = istemciSocket.recv(2048)


print("\nNtp Server'da Saat: " + sunucuZaman.decode("utf-8"))
print("\nGüncellenmiş zaman: " + guncelZaman.decode("utf-8") + " " + zamanDilimi.decode("utf-8"))
z=guncelZaman.decode("utf-8")

zaman=z.split(" ")	
formatliZaman=zaman[0] + " " + zaman[1] + " " + zaman[2] + " " + zaman[3] + " "

print("\nSunucuda soketlerin kapatılmasıyla istemci sistem zamanını güncellemeye hazır hale geldi.\n\n")
os.system('date --set "%s" +\"%%d %%B %%Y %%H:%%M:%%S.%%6N\"' % formatliZaman)
os.system('sudo hwclock -w')




