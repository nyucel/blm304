from socket import *
import pickle
import sys
import os
import time
import select

def get(filename):
    veri , adres= senderSocket.recvfrom(1024)
    dosya = open(filename, 'wb')
    dosya.write(veri)
    dosya.close()
    print("Dosya başarıyla alındı.")

def put(filename):
    dosya = open(filename, 'rb')
    dosya2 = dosya.read()
    senderSocket.sendto(dosya2, (senderIP, senderPort))
    print("Dosya başarıyla yollandı.")

senderIP = input(str("IP adresini giriniz: "))
senderPort = 42

senderSocket = socket(AF_INET, SOCK_DGRAM)
senderSocket.bind((senderIP,senderPort))
Listemiz, addres = senderSocket.recvfrom(1024)
print("Yüklenmiş dosyalar:", Listemiz.decode())

komut=input(str("Almak için GET, koymak için PUT -> Komut seçiniz:  "))
komut2=komut.encode()
senderSocket.sendto(komut2,(senderIP,senderPort))

filename=input(str("Dosya adını giriniz: "))
filename2=filename.encode()
senderSocket.sendto(filename2,(senderIP,senderPort))

if(komut=="GET"):
    get(filename2)
if(komut=="PUT"):
    put(filename)