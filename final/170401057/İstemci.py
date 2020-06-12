# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 19:22:33 2020

@author: shnsr
"""
#Şahan Can sarKI - 170401057
import socket                
import os


# Socket oluşturulması
s = socket.socket()          

# Bağlanılacak adres ve port
host = "192.168.1.42"
port = 142                

try:
    # Bağlantıyı yap
    komut = 'sudo date --set="'
    s.connect((host, port)) 

    # serverden yanıtı al
    server_deneme = s.recv(1024)
    print(server_deneme.decode("utf-8"))

    s.send(server_deneme)   #yanki yolla    
    
    komut = komut + s.recv(1024).decode()[:-4] + '"' #gerekli terminal komutun hazırlanması
    print(komut, 'komut')
    zamandilimi = s.recv(1024)
    print(zamandilimi.decode())
    os.system(komut)                            #komutun çalıştırılması
    s.close() 
except socket.error as msg:
    print("[Server aktif değil.] Mesaj:", msg)
