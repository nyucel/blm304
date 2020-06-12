#Selin Gül 150401040

import socket
from datetime import datetime, timedelta
import time

zaman_dilimi=input("Zaman dilimini giriniz (örneğin UTC +3 için '+3' girin): ")
host=input("Sunucu için IP adresini girin:")
port=142

try:
    soket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soket.bind((host,port))
    soket.listen(5)
    print("142. port dinleniyor")
except socket.error:
    print("Bağlantı hatası oluştu")
while True:
    baglanti,Adres=soket.accept()
    print(' ')
    baglanti.send(str(zaman_dilimi).encode('utf-8')) #istemcinin saati hesaplaması için zaman dililmi gönderilir
    sonAn=time.time()*1000
    baglanti.send(str(sonAn).encode('utf-8'))
    
    zaman_dilimi=int(float(zaman_dilimi))
    print('Milisaniye cinsinden gönderilen zaman: ',sonAn)
    tarih=datetime(1970,1,1)+timedelta(milliseconds=sonAn)+timedelta(hours=zaman_dilimi)
    print('Tarih: ',tarih.strftime("%d/%m/%Y %H:%M:%S.%f"))
    if (zaman_dilimi>=0):
        print('Zaman dilimi: UTC +',zaman_dilimi)
    else:
        print('Zaman dilimi: UTC',zaman_dilimi)
        
    print(" ")
    
    baglanti.close()