#Hakan Reşit YALÇIN - 160401036

import socket
from time import *
import sys

IP  = str(socket.gethostbyname(socket.gethostname()))
print("IP: ",Host)
PORT   = 142

UTC = "UTC+3"
UTCX=UTC[3:] #UTC değişimi için
socketY = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
try:
    socketY.bind((IP, PORT))
except:
    print("Başarısız!")
    sys.exit()
print("Başarılı. Port 142 dinleniyor...")
socketY.listen(1)
while True:
    baglanti = socketY.accept()
    adres = socketY.accept()
    print(adres,"Saat: ",gmtime(time()).tm_hour + int(UTCX),":",gmtime(time()).tm_min,":",gmtime(time()).tm_sec)
    message = baglanti.recv(1024)
    mesaj1 = message.decode()
    if(mesaj1=="Saat"): 
        zaman=int(time()*1000)
        zaman1=str(zaman)+" "+ UTCX
        baglanti.sendall(zaman1.encode())