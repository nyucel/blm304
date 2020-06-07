#Ercan Berber 180401077

import socket
from datetime import datetime
import subprocess
import shlex

PORT = 142
HOST = str(input("Host adresi giriniz..:"))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = (HOST,PORT)
s.connect(server)
gecikme=s.recv(1024).decode()
s.sendall(gecikme.encode())
zaman2=s.recv(1024).decode()
utc=s.recv(1024).decode()
zaman=datetime.fromtimestamp(float(zaman2)/1000)
print(f"{zaman} UTC:{utc}")
time_tuple = (
    zaman.year,
    zaman.month,
    zaman.day,
    zaman.hour,
    zaman.minute,
    zaman.second,
    zaman.microsecond,
)
time_string=datetime(*time_tuple).isoformat()

subprocess.call(shlex.split("timedatectl set-ntp false"))
subprocess.call(shlex.split("sudo date -s '%s'"%time_string))
subprocess.call(shlex.split("sudo hwclock -w"))
