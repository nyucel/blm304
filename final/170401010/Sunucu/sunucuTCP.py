# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 14:50:46 2020

@author: Baran Akçakaya-170401010
"""
import socket
from datetime import datetime

TCP_IP = "192.168.1.35"
TCP_PORT = 142
UTC = 0

try:
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.bind((TCP_IP,TCP_PORT))
    print("Kanal Dinleniyor.")
    sock.listen(5)
except socket.error:
    print("Hata!",socket.error)
    
while(True):
    UTC_ZERO = datetime.utcnow()
    UTC_YEREL = datetime.now()
    gecikme_basla = datetime.now()
    hesap = UTC_YEREL - UTC_ZERO
    hesap = str(hesap).split(",")
    if(len(hesap)>1):
        hesap1 = str(hesap[1]).split(":")
        hesap1 = 24 - int(hesap1[0])
        UTC = 'UTC-'+str(hesap1)
    else:
        hesap1 = str(hesap).split(":")
        UTC = 'UTC+'+str(hesap1[0])[2:]
        
    MESS = str(UTC_YEREL) + ',' + str(UTC)
    data,adr = sock.accept()
    print("------------------------------------")
    print("Cihaz IP:",adr[0])
    print("Cihaz PORT:",adr[1])
    while(True):        
        message = data.recv(1024).decode() 
        if not message:
            break
        print("Gelen Mesaj:",message)
        data.send(MESS.encode())     #gecikme hesaplamak için
        message2 = data.recv(1024).decode() 
        if('True' == message2):
            gecikme_bitir = datetime.now()
            gecikme_zamani = (gecikme_bitir - gecikme_basla)/2
        else:
            print("Hata!")
    
        MESS = str(gecikme_bitir+gecikme_zamani) + ',' + str(UTC)
        print("Mesaj Gönderiliyor...")
        data.send(MESS.encode())    #Tahmini gecikme hesaplanıp eklenerek gönderilen zaman
        print("Mesaj Gönderildi.")
    data.close()
