import socket
from datetime import datetime, timedelta
import os

buf=512
istemci=socket.socket()
host="127.0.0.1"
port=142

try:
    istemci.connect((host,port))
    zaman=istemci.recv(buf).decode('utf-8')
    utc=istemci.recv(buf).decode('utf-8')
    utc=int(utc)
    zaman=float(zaman)
    gecikme=istemci.recv(buf).decode('utf-8')
    gecikme=float(gecikme)
    yTarih2=datetime(1970,1,1)+timedelta(milliseconds=zaman)+timedelta(hours=utc)+timedelta(milliseconds=gecikme)
    sistemKomutu='sudo date -s='+str(yTarih2)
    os.system(sistemKomutu)
        
except socket.error:
    print("hata oluştu")