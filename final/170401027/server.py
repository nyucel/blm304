#! usr/bin/env python
# -- coding: UTF-8 --

#Egemen Inceler

from socket import *
from datetime import datetime,timezone
import calendar
import time
from socket import *
import sys
dt = datetime

sock = socket(AF_INET, SOCK_STREAM)
server_address = ('192.168.1.118', 142)
print ('Ip:  %s port: %s' % server_address)
sock.bind(server_address)

sock.listen(1)

def saatgetir():
	string = str(dt.now().time())
	hour = string[:2]
	minute = string[3:5]
	second = string[6:8]
	ms = string[9:]

	now = (dt.now().time())
	noww=str(dt.now())
	noww = noww[:10]
	tz ="UTC+3"

	num = tz[3:]
	offsetHour = time.timezone / 3600
	offsetHour = offsetHour * (-1)
	diff = offsetHour - int(num)

	dondureleceksaat= int(hour) - int(diff)
	dondurelecekk = str(tz+" "+noww +" "+ str(dondureleceksaat)+":"+str(minute)+":"+str(second)+"."+str(ms))
	return(dondurelecekk)




while True:
    print ('Baglanti bekleniyor.')
    connection, client_address = sock.accept()
    try:
        print ('Baglanti kuruldu.')

        while True:
            data = connection.recv(1024)
            if(data.decode("utf-8")=='ok'):
                	connection.sendall(saatgetir().encode("utf-8"))

            else:
                break
            
    finally:
        connection.close()



