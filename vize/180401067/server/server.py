# UĞUR ALTINTAŞ 180401067

import socket
import os
import sys
import time
import select


def GET(dosyaismi,adres):
    
    try:
        f=open(dosyaismi,"rb")
    except FileNotFoundError:
        print("Dosya bulunamadi")
        UDPServerSocket.sendto("dosya bulunamadı".encode(),adres)
        return
    UDPServerSocket.sendto("dosya bulundu".encode(),adres)
    time.sleep(0.001)
    data=f.read(1024)
    while(data):
        if(UDPServerSocket.sendto(data,adres)):
            data=f.read(1024)
            time.sleep(0.1)
    try:
        kontrol=UDPServerSocket.recv(1024)
    except socket.error:
        print("Bağlantı hatası dosya gönderimi başarısız") 
    f.close()
    

def PUT(dosyaismi,adres):
    f = open(dosyaismi,'wb')
    while True:
        ready = select.select([UDPServerSocket], [], [], 3)
        if ready[0]:
            data= UDPServerSocket.recv(1024)
            f.write(data)
        else:
            print("Dosya İndirildi!")
            
            f.close()
            UDPServerSocket.sendto("kontrol".encode(), adres)
            break
    


Host  = str(socket.gethostbyname(socket.gethostname()))
print(Host)
Port   = 42
bufferSize  = 1024



UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((Host, Port))


print("Bağlantı kuruldu ve port dinlenmeye başlandı")

 
while True:
    clientmesaj = UDPServerSocket.recvfrom(bufferSize)
    mesaj = clientmesaj[0].decode()
    adres = clientmesaj[1]
    
    
    if(mesaj=="ServerListele"):
        listDir = str(os.listdir()).encode()
        
        UDPServerSocket.sendto(listDir,adres)
    elif (mesaj[:3] == "GET"):
        GET(mesaj[4:],adres)
    elif (mesaj[:3] == "PUT"):
        PUT(mesaj[4:],adres)
    time.sleep(1)
