import socket
import sys
import os
import pickle
# Muhammet Burak TURHAN 150401060

UDPIP = input('UDP Sunucusunun IP adresini giriniz: ') 
UDPPORT = 42
max = 4096
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((UDPIP, UDPPORT))

def dosya_listele():

    veri = os.listdir('C:/Users/mbtbr/Desktop/veri')
    et = pickle.dumps(veri)
    s.sendto(et,addr)
    
while True:
    data,addr = s.recvfrom(max)
    gelen = data.decode('UTF-8')
    if (gelen[:7] =='listele'):
        dosya_listele()
    elif (gelen[:3] == 'put'):
        with open('gonderilen.txt', 'wb') as f:
            print('Dosya Yükleniyor, Bekleyiniz!')
            gelendata,addr = s.recvfrom(max)
            if not gelendata:
                break
            f.write(gelendata)
            print('İşleminiz tamamlandı, bağlantı sonlandırılıyor.')
            sys.exit()
    elif (gelen[:3] == 'get'):
        d1 = gelen[4:]
        os.chdir('C:/Users/mbtbr/Desktop/veri')
        d2 = os.listdir('C:/Users/mbtbr/Desktop/veri') 

        if d1 in d2:
            f = open(d1 , 'rb')
            l = f.read(max)
            while (l):
                s.sendto(l,addr)
                print('Gönderiliyor\n ',repr(l))
                l = f.read(max)
                print('İşleminiz tamamlandı, bağlantı sonlandırılıyor.')
                sys.exit()
        else:
            sys.exit()
            print('Dosya bulunamadı, bağlantı sonlandırılıyor.')