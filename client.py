#160401075
#Batuhan METİN

import socket 
import os
from os import sys
from datetime import datetime
import time

ip = input("Sunucunun ip adresi:  ")
port = 142

istemci_socket = socket.socket()
try:
	istemci_socket.connect((ip, port))			
except:
    print("Sunucu bağlantısı kurulmalı.\n")
    sys.exit()
    
print("Sunucu istemci baglantisi saglandi.")

zaman_sunucu = istemci_socket.recv(2048)		
istemci_socket.send(bytes("true", encoding='utf-8'))

zaman_guncel = istemci_socket.recv(2048)		
zaman_dilim = istemci_socket.recv(2048)


print("\nServer'da Saat: " + zaman_sunucu.decode("utf-8"))
print("\nGüncellenmiş zaman: " + zaman_guncel.decode("utf-8") + " " + zaman_dilim.decode("utf-8"))
z=zaman_guncel.decode("utf-8")

zaman=z.split(" ")	
for_zaman=zaman[0] + " " + zaman[1] + " " + zaman[2] + " " + zaman[3] + " "

print("\n Güncelleme Hazır...\n\n")
os.system('date --set "%s" +\"%%d %%B %%Y %%H:%%M:%%S.%%6N\"' % for_zaman)
os.system('sudo hwclock -w')




