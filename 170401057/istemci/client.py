# -*- coding: utf-8 -*-
"""
Created on Sun May 24 20:02:07 2020

@author: shnsr
"""


import socket
import os
import time
 

#msgFromClient       = "Hello UDP Server"

#bytesToSend         = str.encode(msgFromClient)

hedefIp = input("Hedef ip'yi lütfen giriniz : ") #127.0.0.1
localIP     = hedefIp

serverAddressPort   = (localIP, 42)

bufferSize          = 1024


UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


do  = input("Ne Yapmak İstediğinizi Girin (GET veya PUT) = ").encode() #yapılacak işlemi encode ile byte'a çevirip do'ya attık
UDPClientSocket.sendto(do,serverAddressPort)

dataD = UDPClientSocket.recvfrom(bufferSize)[0].decode()
dataD2 = dataD[1:-1]
dataD2 = dataD2.split(", ")

for z in dataD2:
    print(z)

Filename = input("Dosyanın Adını gir : ").encode()

UDPClientSocket.sendto(Filename,serverAddressPort) # GET ve PUT işleminde filename isteği ortak.Onu burda alıp gönderdik.

if( do.decode() == "GET") :
        
        
        file = open(Filename , 'wb')
        file_data = UDPClientSocket.recvfrom(bufferSize)[0]
        try:
            while(file_data):
                file.write(file_data)
                UDPClientSocket.settimeout(2)
                file_data = UDPClientSocket.recvfrom(bufferSize)[0]        
        except socket.timeout:
            
            print("Dosya GET Edildi! ")
        UDPClientSocket.sendto(b'iletildi',serverAddressPort)
        file.close()
        UDPClientSocket.close()
        
    
        
elif (do.decode() == "PUT") :
        
        file = open(Filename.decode() , 'rb')
        file_data = file.read(bufferSize)
        
        while(file_data):
            if(UDPClientSocket.sendto(file_data,serverAddressPort)):
                print("Gönderiliyor")
                file_data = file.read(bufferSize)
                time.sleep(0.001)
        try:
            UDPClientSocket.settimeout(3)
            msg = UDPClientSocket.recvfrom(bufferSize)[0].decode()
            
            if(msg == "iletildi"):
                print('veri başarıyla gönderildi!')
            
            
        except socket.timeout:
            print('veri tam gönderilemedi!')
        UDPClientSocket.close()
        file.close()
        
