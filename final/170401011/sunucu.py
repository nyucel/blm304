#170401011 Berfin Okuducu
import socket
import os
import sys
import datetime
import pickle
import time
host = "127.0.0.1"
port = 142
greenwich=datetime.datetime.utcnow()
zaman=datetime.datetime.now()
baslangic=[zaman.hour,zaman.minute,zaman.second,zaman.microsecond]
utc=zaman.hour-greenwich.hour
if(utc>=0):
    utc="UTC+" + str(utc)
else:
    utc="UTC" + str(utc)
print(zaman,utc)

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("Baglama Basarili")

except :
    print("Baglanti hatasi")
    sys.exit()


s.listen(5)
baglanti, address = s.accept()
simdi=datetime.datetime.now()
liste=[simdi,utc]
zaman_eleman=pickle.dumps(liste)
baglanti.send(zaman_eleman)