#Gökçe Kuler 160401045
import socket
import sys
import os

def denetle(request):
    dosya = open("kaydedilendosya.txt","wb")
    dosya.write(request)
    dosya.close()

soket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)    
udp_port = 42                                  
blocksize=4096
soket.bind(('0.0.0.0',udp_port))

while True:

    print ("İstemci bekleniyor")
    data,addr = soket.recvfrom(1024)           
    print ("İstemci mesajı:",data,addr)
    dizin=os.getcwd()
    listele=os.listdir(dizin)
    str1=","
    listeleme2=str1.join(listele)
    soket.sendto(listeleme2.encode(),addr) #sunucu dizininde bulunan dosya isimlerini istemciye gönderir
    metod,addr=soket.recvfrom(1024)	   #istemciden gelen get ve put metodunu alır
    if(metod==b'GET'):
        veri,addr = soket.recvfrom(1024)
        cekilen=veri[4:13]
        if os.path.exists("cekilecek"):
            with open("cekilecek","rb") as f:
                icerik = f.read(blocksize)
                while icerik != '':
                    soket.sendto(icerik,addr) 
                    icerik = f.read(blocksize)
                    print("Dosya istemciye gönderildi")
                    break

    if(metod==b'PUT'):
        veri,addr = soket.recvfrom(1024)  #sunucudan gelen dosyanın içeriğini alır
        denetle(veri)


