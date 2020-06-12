import socket
from time import *
import sys
Host  = str(socket.gethostbyname(socket.gethostname()))
print("Sunucu ip adresi: ",Host)
Port   = 142
bufferSize  = 1024
UTC = "UTC+3"
UTCdegis=UTC[3:]
TCPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
try:
    TCPServerSocket.bind((Host, Port))
except:
    print("Sunucu oluşturulamadı")
    sys.exit()
print("Bağlantı kuruldu ve port dinlenmeye başlandı")
TCPServerSocket.listen(1)
while True:
    connection, client_address = TCPServerSocket.accept()
    print(client_address,"Saat: ",gmtime(time()).tm_hour + int(UTCdegis),":",gmtime(time()).tm_min,":",gmtime(time()).tm_sec)
    clientmesaj = connection.recv(bufferSize)
    mesaj = clientmesaj.decode()
    if(mesaj=="Saat"): 
        saat=int(time()*1000)
        saat1=str(saat)+" "+ UTCdegis
        connection.sendall(saat1.encode())
