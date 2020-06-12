#Selin Gül 150401040

import socket
from datetime import datetime, timedelta
import os, sys
import time

buf=512
soket=socket.socket()
host=input("Bağlanmak istediğiniz IP adresini girin:")
port=142

try:
    soket.connect((host,port))

    zaman_dilimi=soket.recv(buf).decode('utf-8')
    ilkMesaj=time.time()*1000 #ikinci mesaj gelmeden önce
    
    sonAn=soket.recv(buf).decode('utf-8')
    sonMesaj=time.time()*1000 #ikinci mesaj geldikten sonra
    
    f=float(sonAn)
    
    fark=sonMesaj-ilkMesaj
    
    zaman_dilimi=int(float(zaman_dilimi))
    
    zamanHesapla=datetime(1970,1,1)+timedelta(milliseconds=f)+timedelta(hours=zaman_dilimi)+timedelta(milliseconds=fark)
    gecikmeliZaman=zamanHesapla.strftime("%d/%m/%Y %H:%M:%S.%f")
    #komut için hesaplanan tarih = epoch(1970,1,1) + milisaniye cinsinden gelen zaman + zaman dilimi + hesaplanan gecikme süresi
    komut='sudo date --set="'+str(zamanHesapla)+'"'
    
    if sys.platform=='linux2' or sys.platform=='linux':
        os.system(komut)
     
    print(" ")
    print('Milisaniye cinsinden gelen zaman: ',f)
    if (zaman_dilimi>=0):
        print('Gelen zaman dilimi: UTC +',zaman_dilimi)
    else:
        print('Gelen zaman dilimi: UTC',zaman_dilimi)
        
    print('Gecikmeli zaman:',gecikmeliZaman)
    print('Komut:', komut)      
    print(" ")    
except socket.error:
    print("Bağlantı hatası oluştu")