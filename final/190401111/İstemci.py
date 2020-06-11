#190401111-Atahan Aktaş

import socket                
import os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     #Soket Oluşturma TCP     

host = "192.168.1.9" #Özel Kullanım IP
port = 142   #TCP port 142 kullanmalı            

try:
    k = 'sudo date --s '
    s.connect((host, port))    #Bağlantı

    cevap = s.recv(1024)
    print(cevap.decode('utf-8'))  #Yanıt

    s.send(cevap)   
      
    k = k + s.recv(1024).decode() + '"'
    print(k)
    zamann = s.recv(1024)               #Zaman Dilimi (UTC+2 veya UTC-3 Gibi)
    print(zamann.decode())
    os.system(k)                
    s.close() 

except socket.error as msg:
    print("Hata", msg)
