# -*- coding: utf-8 -*-
"""
Created on Sun May 24 20:02:07 2020

@author: shnsr
"""


import socket
import os
import time



localIP = input("sunucu IP adresini girin = ")

localPort   = 42

bufferSize  = 1024

klasör = os.listdir()

x = "server files"
if x not in klasör:
    os.mkdir(x)
else:
    print("Serves Files Zaten Var..")
os.chdir(x)

while(True):
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) #UDP için sunucu Socketini oluşturduk.

    UDPServerSocket.bind((localIP, localPort)) #belirlediğimiz ip ve porta bağladık.
    
    do,do2 = UDPServerSocket.recvfrom(bufferSize) # yapılacak işlemi burda aldık
    do = do.decode()
    print(do)
    address2 = do2

   
    
    ornekD = os.getcwd()
    ornekD2 = str(os.listdir())
    ornekD2 = ornekD2.encode()

    UDPServerSocket.sendto(ornekD2,address2)  
    
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    
    fileName = bytesAddressPair[0] # asıl gönderilen veri burda
    address = bytesAddressPair[1] # gönderilen veri için addressi burda aldık
    
    print("UDP server dinlemeye başladı....")
    
    
    if(do == "GET"):
        

        
        file = open(fileName.decode() , 'rb')

        file_data = file.read(bufferSize)
        
        while(file_data):
            if(UDPServerSocket.sendto(file_data,address)):
                print("Dosya alınıyor...")
                file_data = file.read(bufferSize)
                time.sleep(0.001)
        try:
            UDPServerSocket.settimeout(3)
            msg = UDPServerSocket.recvfrom(bufferSize)[0].decode()
            
            if(msg == "iletildi"):
                print('veri başarıyla gönderildi!')
            
            
        except socket.timeout:
            print('veri tam gönderilemedi!')
        file.close()
            
            
    elif(do == "PUT"):
        
        file = open(fileName , 'wb')
        file_data = UDPServerSocket.recvfrom(bufferSize)[0]         #recfrom ile veriyi dinliyoruz (byte şekklinde)
        try :
            while(file_data):
                file.write(file_data)
                UDPServerSocket.settimeout(2)               #süre zarfında veri gelmezse dinlemeyi kesiyoruz .
                file_data = UDPServerSocket.recvfrom(bufferSize)[0]
                
        except socket.timeout:
            print("Dosya PUT Edildi! ")
        UDPServerSocket.sendto(b'iletildi',address)
        file.close()
        
    else:
        print("Bilinmeyen bir işlem isteğinde bulundunuz...")
            
    
    
    
