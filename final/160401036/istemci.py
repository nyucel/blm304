#Hakan Reşit YALÇIN - 160401036	

import socket
from time import *
from timeit import default_timer as timer
import sys
import subprocess
import shlex
from _datetime import datetime

host = input("Sunucu IP giriniz: "))   
port = 142


socketX = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

try:
	socketX.connect(host,port)
        print("Bağlantı başarılı!")
        break

except:
        print("Bağlantı başarısız!")
        sys.close()
    
socketX.send("0".encode())

ilk=timer()
data = socketX.recv(1024).decode().split(" ")
son=timer()

gecikme=son-ilk

sa=int(data[0])
UTC=data[1]

print("Saat: ",sa," ms"," UTC",UTC)

yil=gmtime(sa/1000).tm_year
ay=gmtime(sa/1000).tm_mon
gun=gmtime(sa/1000).tm_mday
st=gmtime(sa/1000).tm_hour + int(UTC)
dk=gmtime(sa/1000).tm_min
sn=gmtime(sa/1000).tm_sec

milisn=sa%1000+gecikme

tarih=(int(yil),int(ay),int(gun),int(st),int(dk),int(sn),int(milisn))
date=datetime(*tarih).isoformat()

subprocess.call(shlex.split("timedatectl set-ntp false"))
subprocess.call(shlex.split("sudo date -s '%s'" % date))
subprocess.call(shlex.split("sudo hwclock -w"))