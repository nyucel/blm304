import socket
import os
import sys
import datetime
import pickle
import time

host = "127.0.0.1"
port = 142


#Zamanı ve UTC'yi hesaplama bölümü
greenwich=datetime.datetime.utcnow()
zaman=datetime.datetime.now()
baslangic=[zaman.hour,zaman.minute,zaman.second,zaman.microsecond]
utc=zaman.hour-greenwich.hour
if(utc>=0):
    utc="UTC+" + str(utc)
else:
    utc="UTC" + str(utc)
print(zaman,utc)

#Zamanı liste haline getiriyoruz

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket {} nolu porta bağlandı".format(port))

except socket.error as msg:
    print("Hata:",msg)


#Zamanı liste şeklinde istemci'ye yolluyoruz.
s.listen(5)
connection, client_address = s.accept()
simdizaman=datetime.datetime.now()
zamanliste=[simdizaman,utc]
eleman=pickle.dumps(zamanliste)
connection.send(eleman)





