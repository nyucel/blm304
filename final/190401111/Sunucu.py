#190401111-Atahan Aktaş

import socket
from datetime import datetime, timedelta

def gecikmee(): #Gecikmeyi Hesaba Katmalıyız
    
    zaman = datetime.utcnow() + timedelta(hours = utc) 
    zaman2 = str(zaman)
    
    yil = zaman2[:4]
    zaman2 = zaman2[5:]
    
    ay = zaman2[:2]
    zaman2 = zaman2[3:]
    
    gun = zaman2[:2]
    zaman2 = zaman2[3:]
    
    zaman2 = gun + '/' + ay + '/' + yil + ' ' + zaman2
    c.send(zaman2[:-3].encode('utf-8')) 
    
    karsilik = c.recv(1024)                             
    
    zamanyeni = datetime.utcnow() + timedelta(hours = utc)  #Zaman Farkı
    gecikme = (zamanyeni - zaman) / 2                      
    
    print(gecikme, 'Gecikme')
    return gecikme

def yeniSaat(gecikme):              

    zaman = datetime.utcnow() + timedelta(hours = utc) + gecikme
    zaman2 = str(zaman)
    
    yil = zaman2[:4]
    zaman2 = zaman2[5:]
    
    ay = zaman2[:2]
    zaman2 = zaman2[3:]
    
    gun = zaman2[:2]
    zaman2 = zaman2[3:]

    zaman2 = gun + '/' + ay + '/' + yil + ' ' + zaman2
    zaman2 = zaman2[:-3]
    return zaman2.encode()

host = "192.168.1.9"  #Özel Kullanım IP
port = 142     #TCP port 142 kullanmalı
utc = 3       #Zaman Dilimi

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #TCP
    print("Soket Oluşturuldu")
    
    s.bind((host, port)) 
    print("Soket {} Nolu Porta Bağlandı.".format(port))
    
    s.listen(1)      
    
except socket.error as msg:
    print("Hata",msg)

while True: 
    c, addr = s.accept()      
    print('Bağlantı:', addr)
    gecikme = gecikmee()
    d = yeniSaat(gecikme)
    c.send(d)
    zamann = 'utc' + str(utc)
    c.send(zamann.encode())
    c.close()
