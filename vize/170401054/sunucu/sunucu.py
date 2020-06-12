import socket
import time
import sys
import os

IP = "127.0.0.1"
PORT = 42

def dosyala():
    adlar = os.listdir()
    liste = []
    for dosya in adlar:
        liste.append(dosya)
    liste = str(liste)
    liste = liste.encode()
    print(liste)
    sock.sendto(liste, (IP, PORT))

def get(file_name):
    f = open(file_name, "rb")
    veri = f.read()
    s.sendto(veri, (IP,PORT))
    print("Dosya başarıyla alındı.")

                
def  put(file_name):
    veri, address = sock.recvfrom(1024)
    dosya = open(file_name, 'wb')
    dosya.write(veri)
    dosya.close()
    print("Dosya başarıyla koyuldu.")
        
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("bağlandı.")
dosyala()

komut,adr1=sock.recvfrom(1024)
komut=komut.decode()


if(komut=="GET"):
    filename, adr2 = sock.recvfrom(1024)
    filename = filename.decode()
    get(filename)
elif(komut=="PUT"):
    filename, adr2 = sock.recvfrom(1024)
    filename = filename.decode()
    put(filename)



