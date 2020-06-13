#MelisGüler160401049
import socket
import datetime
from datetime import datetime

TCP_IP = "192.168.1.35"
TCP_PORT = 142
UTC = 0

try:
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((TCP_IP,TCP_PORT))
    s.listen(5)
except socket.error:
    print("Hata!",socket.error)
    
while(True):
    UTC1 = datetime.utcnow()
    UTC2 = datetime.now()
    g_baslangic = datetime.now()
    sonuc = UTC2 - UTC1
    sonuc = str(sonuc).split(",")
    if(len(sonuc)>1):
        s1 = str(sonuc[1]).split(":")
        s1 = 24 - int(s1[0])
        UTC = 'UTC-'+str(s1)
    else:
        s1 = str(sonuc).split(":")
        UTC = 'UTC+'+str(s1[0])[2:]
        
    g = str(UTC2) + ',' + str(UTC)
    veri,adres = s.accept()
    print("IP:",adres[0])
    print("PORT:",adres[1])
    while(True):        
        mesaj = veri.recv(1024).decode() 
        if not mesaj:
            break
        veri.send(g.encode())
        mesaj2 = veri.recv(1024).decode() 
        if('True' == mesaj2):
            g_bitis = datetime.now()
            g_süresi = (g_bitis - g_baslangic)/2
        else:
            print("HATA!")
        g = str(g_bitis+g_süresi) + ',' + str(UTC)
        print("Mesaj Gönderildi.")
    data.close()