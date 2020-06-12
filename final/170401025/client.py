import socket
import ntplib
import time
import subprocess
import shlex
import pickle
import datetime
from datetime import datetime


başlama_saati=datetime.now()
soket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host="localhost"
port=142
soket.connect((host,port))
data=soket.recv(1024)
print(data)
mesaj="istemci tarafi basarili"
mesaj1=mesaj.encode('utf-8')
soket.sendto(mesaj1,(host,port))
print("\nZaman bekleniyor.")
print("Milisaniye:")
data2=soket.recv(1024)
print(data2)

zaman,address=soket.recvfrom(1024)
zaman=pickle.loads(zaman)
zaman=zaman[0]
bitme_saati=datetime.now()
gecen_zaman=bitme_saati.microsecond-başlama_saati.microsecond

eklenecek_zaman = datetime(zaman.year,zaman.month,zaman.day,zaman.hour,zaman.minute,zaman.second,zaman.microsecond+gecen_zaman).isoformat()
subprocess.call(shlex.split("timedatectl set-ntp false"))
subprocess.call(shlex.split("sudo date -s '%s'" % eklenecek_zaman))
subprocess.call(shlex.split("sudo hwclock -w"))

soket.close()