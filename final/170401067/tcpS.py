# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 22:15:56 2020

@author: EnesNK
"""

import socket
from datetime import datetime, timedelta


def gecikmeHesapla():                                   #bağlantının gecikmesinin hesaplanması(düzenlenme işlemlerinin burada da yapılmasının sebebi düzenlemelerin yaptığı gecikmeyi de hesaplamak)
    
    zaman = datetime.utcnow() + timedelta(hours= utc) 
    zamanDuzenli = str(zaman)
    yil = zamanDuzenli[:4]
    zamanDuzenli = zamanDuzenli[5:]
    ay = zamanDuzenli[:2]
    zamanDuzenli = zamanDuzenli[3:]
    gun = zamanDuzenli[:2]
    zamanDuzenli = zamanDuzenli[3:]
    zamanDuzenli = ay + '/' + gun +'/' + yil + ' ' + zamanDuzenli
    c.send(zamanDuzenli[:-3].encode('utf-8')) 
    
    yanki = c.recv(1024)                                #mesajın yankısı gelene kadar hesaplamayı bekletiyorum
    
    zaman2 = datetime.utcnow() + timedelta(hours= utc)  #yankıdan hemen sonra süre farkını alıyorum
    gecikme = (zaman2 - zaman) / 2                      #verinin geri gelme süresini çıkardım
    
    print(gecikme, 'gecikme')
    return gecikme

def ilerletilmisSaat(gecikme):                          #gecikmeyi saatimize ekleyiyoruz ardından veriyi düzenleyip gönderiyoruz.
    zaman = datetime.utcnow() + timedelta(hours= utc) + gecikme

    zamanDuzenli = str(zaman)
    yil = zamanDuzenli[:4]
    zamanDuzenli = zamanDuzenli[5:]
    ay = zamanDuzenli[:2]
    zamanDuzenli = zamanDuzenli[3:]
    gun = zamanDuzenli[:2]
    zamanDuzenli = zamanDuzenli[3:]

    zamanDuzenli = ay + '/' + gun +'/' + yil + ' ' + zamanDuzenli
    zamanDuzenli = zamanDuzenli[:-3]
    return zamanDuzenli.encode()

host = "192.168.1.32"
port = 142
utc = 3

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("socket oluşturuldu")
    
    s.bind((host, port)) 
    print("socket {} nolu porta bağlandı".format(port))
    
    s.listen(1)      
    print("socket dinleniyor")
except socket.error as msg:
    print("Hata:",msg)

while True: 

    c, addr = s.accept()      
    print('Gelen bağlantı:', addr)
    gecikme = gecikmeHesapla()
    data = ilerletilmisSaat(gecikme)
    c.send(data)
    c.close()
