Python 3.8.3 (tags/v3.8.3:6f8c832, May 13 2020, 22:20:19) [MSC v.1925 32 bit (Intel)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> 
#150401014 Furkan DEMİR

import socket
import sys
import os
import pickle

HOST = input('UDP Sunucusunun IP adresini giriniz: ') 
PORT = 42
socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
socket.bind((HOST, PORT))

def dosyaList():

    txt = os.listdir('C:/Users/demir/Desktop/vh')
    dosya = pickle.dumps(txt)
    socket.sendto(dosya,addr)
    
while True:
    data,addr = socket.recvfrom(1024)
    gelen = data.decode('UTF-8')
    if (gelen[:4] =='listele'):
        dosyaList()
    elif (gelen[:3] == 'put'):
        with open('recv.txt', 'wb') as file:
            print('Dosya Yükleniyor, Bekleyiniz!')
            gelendata,addr = socket.recvfrom(1024)
            if not gelendata:
                break
            file.write(gelendata)
            print('İşleminiz tamamlandı, bağlantı sonlandırılıyor.')
            sys.exit()
    elif (gelen[:3] == 'get'):
        d1 = gelen[4:]
        os.chdir('C:/Users/demir/Desktop/vh')
        d2 = os.listdir('C:/Users/demir/Desktop/vh') 

        if d1 in d2:
            file = open(d1 , 'rb')
            l = file.read(1024)
            while (l):
                socket.sendto(l,addr)
                print('Gönderiliyor\n ',repr(l))
                l = file.read(1024)
                print('İşleminiz tamamlandı, bağlantı sonlandırılıyor.')
                sys.exit()
        else:
            sys.exit()
            print('Dosya bulunamadı, bağlantı sonlandırılıyor.')