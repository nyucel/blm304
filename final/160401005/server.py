# Gizem Karagöl
import socket 
import time
from datetime import datetime 
import locale

locale.setlocale(locale.LC_ALL, '')

# Server bilgileri
ip = input("\ Server icin IP adresini giriniz...")
port = 142
utc= +3

try:
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((ip,port))
print("IP: ",ip," ", port, ".port dinleniyor...")
server.listen(5)

except socket.error as message:
print("hata !", message )

#istemci ile baglantı kuruluyor
while True:
c,addr = server.accept()
print( "connection address : ", addr)
simdiki = datetime.datetime.now()

baslangic = datetime.datetime.timestamp(simdiki)

zaman= str(baslangic)
c.send(zaman.encode())
server.close()


