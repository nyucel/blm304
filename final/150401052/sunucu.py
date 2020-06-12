#Erdin ALHAS 150401052

import socket, os, time, sys
from datetime import datetime, timezone, timedelta

port = 142
SIZE = 2048
ip = ""

s_soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_soket.bind((ip, port))
s_soket.listen(1)
istemci, istemciAdres = s_soket.accept()

UTC = int(input("Zaman dilimini seciniz: UTC ")) 
if (UTC < 0):
    print("\nSecilen zaman dilimi:UTC -" + str(UTC))
else:
    print("\nSecilen zaman dilimi:UTC +" + str(UTC))
if (UTC < 0):
        timezone = " UTC " + str(UTC)
else:
        timezone = " UTC +" + str(UTC)

ilkZaman = datetime.utcnow() + timedelta(hours=UTC)
istemci.send(bytes(str(ilkZaman) + timezone, encoding='utf-8'))  
kontrol = istemci.recv(SIZE)  
sonZaman = datetime.utcnow() + timedelta(hours=UTC)
gidisDonus = sonZaman - ilkZaman
gecikme = gidisDonus / 2 
print("Gecikme Suresi: ", gecikme)

zaman = datetime.utcnow() + timedelta(hours=UTC)+gecikme  
zaman = str(zaman.strftime("%d %B %Y ")) + str(datetime.time(zaman))

istemci.send(bytes(zaman, encoding='utf-8'))
print("\nGecikmeli Sunucu Zamani: ", zaman)

if (UTC < 0):
    timezone = " UTC " + str(UTC)
else:
    timezone = " UTC +" + str(UTC)

istemci.send(bytes(timezone, encoding='utf-8'))
istemci.close()
s_soket.close()