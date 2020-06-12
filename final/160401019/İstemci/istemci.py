import socket
import time
import subprocess
import shlex
import pickle
from datetime import datetime

#160401019
#Sena Günay

host = "127.0.0.1"
port = 142


ilk_zaman=datetime.now() 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host,port))

istemci_mesaj = ('istemci baglandi').encode('utf-8')
client.sendto(istemci_mesaj, (host,port))

mesaj,adrr = client.recvfrom(1024)
print(mesaj)


zaman,adres=client.recvfrom(1024)
zaman=pickle.loads(zaman)
zaman=zaman[0]
bitis_zamani=datetime.now() 
sonzaman=bitis_zamani.microsecond - ilk_zaman.microsecond
sureyiekle = datetime(zaman.year,zaman.month,zaman.day,zaman.hour,zaman.minute,zaman.second,zaman.microsecond+sonzaman).isoformat()
subprocess.call(shlex.split("timedatectl set-ntp false"))
subprocess.call(shlex.split("sudo date -s '%s'" % sureyiekle))
subprocess.call(shlex.split("sudo hwclock -w"))

