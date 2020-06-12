
#----Şamil--GÜVEN--160401038---- 

import socket
import time
from datetime import datetime, timezone, timedelta
import sys


UTC = +3
port = 142


host = input("Server IP Giriniz : ")


def gecikmeSuresi(istemci):
    ilkZaman = datetime.utcnow() + timedelta(hours = UTC)
    istemci.send(bytes(str(ilkZaman), encoding='utf-8'))
    kontrol = istemci.recv(128)
    sonZaman = datetime.utcnow() + timedelta(hours = UTC)
    gecikme = (sonZaman - ilkZaman) / 2
    print("Gecikme:", gecikme)
    return gecikme

with socket.socket() as s:
    try:
        
        s.bind((host, port))
    except:
        print("HATA: Sunucu olusturma başarısız oldu. Tekrar deneyiniz..")
        sys.exit()



    print("------- Sunucu çalışıyor -------")
    while True:
        s.listen()
        con, addr = s.accept()
        with con:
            while True:
                data = con.recv(128)
                if not data:
                    break
                gecikme = gecikmeSuresi(con)
                zaman = datetime.utcnow() + timedelta(hours = UTC) + gecikme
                con.send(bytes(str(zaman), encoding='utf-8'))
                
    s.close()                
                
                
         
              
