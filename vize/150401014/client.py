# 150401014 Furkan DEMİR
import socket
import sys
import os
import pickle

HOST = input('Sunucu IP: ')
PORT = 42
ADDR = (HOST,PORT)
socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

while True:
    message = input('\n Liste komutunu ile dizini listeleyebilirsiniz\n PUT dosya adı ile dosya yükleyebilirsiniz\n GET dosya adı ile dosya indirebilirsiniz\n')
    socket.sendto(message.encode('UTF-8'),ADDR)
    if(message[:4] == 'liste'):
        dizin,addr = socket.recvfrom(1024) 
        dizinList = pickle.loads(dizin)
        print(dizinList)
    elif(message[:3] == 'put'):
        os.chdir('C:/Users/demir/Desktop/vhclient')
        d = os.listdir('C:/Users/demir/Desktop/vhclient')
        if message[4:] in d:
            dosya = message[4:]

            file= open(dosya,'rb')
            l = file.read(1024)
            while (l):
                socket.sendto(l,ADDR)
                print('Gönderiliyor\n ',repr(l))
                l = file.read(1024)
                print('İşleminiz tamamlandı, bağlantı sonlandırılıyor.')
                sys.exit()
        else:
            print('Dosya mevcut değil!')
    elif(message[:3] == 'get'):

        with open('recv.txt', 'wb') as file:
            print('Dosya yükleniyor...')
            data,addr = socket.recvfrom(1024)
            if not data:
                break
            file.write(data)
            print('İşleminiz tamamlandı, bağlantı sonlandırılıyor.')
            sys.exit()
    else:
        print('Böyle bir komut bulunamadı!')
