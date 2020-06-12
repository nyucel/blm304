# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 19:23:05 2020

@author: shnsr
"""
#Şahan Can sarKI - 170401057
import socket
from datetime import datetime, timedelta


host = "192.168.1.42"
port = 142
girilen_UTC = 4

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("UDP Socket oluşturuldu")
    
    s.bind((host, port)) 
    print("UDP Socket {} nolu porta bağlandı".format(port))
    s.listen(1)
    print("socket dinleniyor")
except socket.error as msg:
    print("Hata:",msg)

while True: 

    c, addr = s.accept()      
    print('Gelen bağlantı:', addr)
    
    time1 = datetime.utcnow() + timedelta(hours= girilen_UTC)
    time2 = str(time1)
    print(time1)
    time_yil = time2[:4]
    time_ay = time2[5:7]
    time_gun = time2[8:10]
    time_saat = time2[11:13]
    time_dakika = time2[14:16]
    time_saniye = time2[17:19]
    time_milisaniye = time2[20:26]
        #print(time_yil,time_ay,time_gun,time_saat,time_dakika,time_saniye,time_milisaniye)
        
    time_terminal = time_yil + "-" + time_ay + "-" + time_gun + " " + time_saat + ":" + time_dakika + ":" + time_saniye + "." + time_milisaniye
    c.send(time_terminal.encode('utf-8'))
        
    geri_donus = c.recvfrom(1024)
    #time.sleep(6)   
    time_second = datetime.utcnow() + timedelta(hours=girilen_UTC) 
    time_gecikme = (time_second - time1) / 2 
    print(time_gecikme, ' ----------> Gecikme Süresi')
    
    time3 = datetime.utcnow() + timedelta(hours= girilen_UTC)
    time4 = str(time3)
    print(time3)
    time_yil = time4[:4]
    time_ay = time4[5:7]
    time_gun = time4[8:10]
    time_saat = time4[11:13]
    time_dakika = time4[14:16]
    time_saniye = time4[17:19]
    time_milisaniye = time4[20:26]
        
    gecikme_saniye = str(time_gecikme)[5:7]
    gecikme_saniye = int(gecikme_saniye)
    time_saniye = int(time_saniye)
    time_saniye += gecikme_saniye
    
    if(time_saniye < 10):
        time_saniye = "0" + str(time_saniye)
    else:
        time_saniye = str(time_saniye)
    
    time_terminal2 = time_yil + "-" + time_ay + "-" + time_gun + " " + time_saat + ":" + time_dakika + ":" + time_saniye + "." + time_milisaniye
    print(time_terminal2, 'deneme')
    c.send(time_terminal2.encode('utf-8'))
    zaman = 'utc' + str(girilen_UTC)
    c.send(zaman.encode())
    c.close()
    
