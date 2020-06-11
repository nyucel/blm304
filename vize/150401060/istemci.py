import socket
import sys
import os
import pickle
# Muhammet Burak TURHAN 150401060

UDPIP = input('Bağlanmak istediğiniz sunucu IP: ')
UDPPORT = 42
max = 4096
ADDR = (UDPIP, UDPPORT)
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

while True:
    message = input('\n1. Sunucudaki dosyaları listelemek için listele\n2. Sunucuya dosya yüklemek için put dosya adı\n3. Sunucudan dosya indirmek için get dosya adı\n')
    s.sendto(message.encode('UTF-8'),ADDR)
    if(message[:7] == 'listele'):
        veri,addr = s.recvfrom(max) 
        veridizi = pickle.loads(veri)
        print(veridizi)
    elif(message[:3] == 'put'):
        os.chdir('C:/Users/mbtbr/Desktop/veri2')
        d = os.listdir('C:/Users/mbtbr/Desktop/veri2')
        if message[4:] in d:
            dosya = message[4:]

            f= open(dosya,'rb')
            l = f.read(max)
            while (l):
                s.sendto(l,ADDR)
                print('Gönderiliyor\n ',repr(l))
                l = f.read(max)
                print('İşleminiz tamamlandı, bağlantı sonlandırılıyor.')
                sys.exit()
        else:
            print('Dosya mevcut değil!')
    elif(message[:3] == 'get'):

        with open('gelendosya.txt', 'wb') as f:
            print('Dosya yükleniyor...')
            veri2,addr = s.recvfrom(max)
            if not veri2:
                break
            f.write(veri2)
            print('İşleminiz tamamlandı, bağlantı sonlandırılıyor.')
            sys.exit()
    else:
        print('Böyle bir komut bulunamadı!')