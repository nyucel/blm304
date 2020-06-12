#Adem YILMAZ - 160401069
import socket
import sys
import datetime
import pickle
host = "127.0.0.1"
port = 142
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("Baglama Basarili")

except :
    print("Baglanti hatasi")
    sys.exit()

greenwich=datetime.datetime.utcnow()
timee=datetime.datetime.now()
baslangic=[timee.hour,timee.minute,timee.second,timee.microsecond]
utc=timee.hour-greenwich.hour
utc="UTC+" + str(utc)



s.listen(5)
conn, addr = s.accept()
suan=datetime.datetime.now()
liste=[suan,utc]
zaman=pickle.dumps(liste)
conn.send(zaman)