# Enes TEKİN 150401032

import socket
import sys
import os
import pickle


IP = input('Bağlanmak istediğiniz sunucu IP: ')
PORT = 42
buf = 2048
ADDR = (IP,PORT)

client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

while True:

    cmd = input('\n1. Sunucu listesini listelemek için liste yazınız\n2. Sunucuya dosya eklemek için PUT dosya adı giriniz\n3. Sunucudan dosya indirmek için GET dosya adı giriniz\n') #GET transferfile.txt PUT transferfile.txt gibi
    client.sendto(cmd.encode('UTF-8'),ADDR)

    if(cmd[:3] == 'lis'):
        ldata,addr = client.recvfrom(buf) 
        data_arr = pickle.loads(ldata)
        print(data_arr)

    elif(cmd[:3] == 'PUT'):

        os.chdir('c:/Users/Enes TEKIN/Desktop/client')
        dosyalar = os.listdir('c:/Users/Enes TEKIN/Desktop/client') #göndereceğimiz dosyanın yolunu giriyoruz

        if cmd[4:] in dosyalar:
            dosyaAdi = cmd[4:]

            f= open(dosyaAdi,'rb')
            l = f.read(buf)
            while (l):
                client.sendto(l,ADDR)
                print('Gönderiliyor\n ',repr(l))
                l = f.read(buf)
                print('Tamamlandı')
                print('Bağlantı kapatılıyor')
                sys.exit()
                
        else:
            print('Böyle bir dosya bulunamadı')

    elif(cmd[:3] == 'GET'):

        with open('gelendosya.txt', 'wb') as f:
            print('Dosya alınıyor...')
            gdata,addr = client.recvfrom(buf)
            if not gdata:
                break
            f.write(gdata)
            print('Tamamlandı')
            print('Bağlantı kapatılıyor') 
            sys.exit()
                

    else:
        print('Geçersiz komut girdiniz')
        