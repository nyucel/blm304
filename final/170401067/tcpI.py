# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 22:26:03 2020

@author: EnesNK
"""

import socket                
import os


# Socket oluşturulması
s = socket.socket()          

# Bağlanılacak adres ve port
host = "192.168.1.32"
port = 42                

try:
    # Bağlantıyı yap
    komut = 'sudo date --set="'
    s.connect((host, port)) 

    # serverden yanıtı al
    yanit = s.recv(1024)
    print(yanit.decode("utf-8"))

    s.send(yanit)   #yanki yolla
    # bağlantıyı kapat
    
    
    komut = komut + s.recv(1024).decode() + '"' #gerekli terminal komutun hazırlanması
    print(komut)
    zamandilimi = s.recv(1024)
    print(zamandilimi.decode())
    os.system(komut)                            #komutun çalıştırılması
    s.close() 
except socket.error as msg:
    print("[Server aktif değil.] Mesaj:", msg)
