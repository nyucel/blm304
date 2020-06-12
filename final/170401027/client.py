#! usr/bin/env python
# -- coding: UTF-8 --

#Egemen Inceler

from socket import *
from datetime import datetime, timezone
import calendar
import time
import sys
import os	

sock = socket(AF_INET, SOCK_STREAM)

server_address = ('192.168.1.118', 142)
print ('Ip adresi:  %s port: %s' % server_address)
sock.connect(server_address)
dt = datetime
try:
    
    message = ('ok')
    sock.sendall(message.encode("UTF-8"))
    first_ms = str(dt.now().time())[6:]
    time = sock.recv(1024).decode("UTF-8")
    print ('Gelen sistem saati: "%s"' % time)
    second_ms = str(dt.now().time())[6:]
    current = float(time[23:]) + (float(second_ms)-float(first_ms))

    if(int(time[3:5]) < 0):
    	a = "sudo date --s "+'"'+str(time[6:22])+str(current)+'"'
    else:
    	a = "sudo date --s "+'"'+str(time[6:22])+":"+str(current)+'"'
    print("\nAyarlanan sistem saati: ",str(time[6:22])+":"+str(current))
    os.system(a)
finally:
    print ('Socket kapatiliyor.')
    sock.close()