import socket
import os
from time import gmtime,strftime
import time
import datetime
import sys
#MELİSA BAYRAMLI 140401052


BUFFERSIZE=1024
host=str(socket.gethostbyname(socket.gethostname()))
port = 142

print("Host= ",host)
print("Port= ",port)

try:
    tcp_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print("Server ile baglanti kuruluyor..")
    tcp_socket.connect((host,port))

except:
    print("BAĞLANAMADI...",socket.error)
    sys.exit()

komut = 'sudo date --set='
msg=tcp_socket.recv(BUFFERSIZE)
print(msg.decode())
tcp_socket.sendto("zaman".encode(),(host,port))
msg=tcp_socket.recv(BUFFERSIZE)
tarih=msg.decode().split(' ')
msg=tarih[0]
print(msg)
s = float(msg) / 1000.0
saat = datetime.datetime.fromtimestamp(s).strftime('%m/%d/%Y %H:%M:%S.%f')

print(saat)
komut = komut + '"' + saat + '"'
print(komut, 'komut')
os.system(komut)
tcp_socket.close()