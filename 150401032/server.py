#Enes TEKİN 150401032

import socket
import sys
import os
import pickle
import shutil

IP = input('Server IP: ') 
PORT = 42
buf = 2048

server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server.bind((IP,PORT))

def serverList():

    dizin = os.listdir('c:/Users/Enes TEKIN/Desktop/dizin') #dizinin bulunduğu yolu parametre olarak yazınız.
    et = pickle.dumps(dizin)
    server.sendto(et,addr)


while True:
    
    data,addr = server.recvfrom(buf)
    cmd = data.decode('UTF-8')

    if (cmd[:3] =='lis'):
        serverList()                              

    elif (cmd[:3] == 'PUT'):

        with open('gelendosya.txt', 'wb') as f:
            print('Dosya alınıyor...')
            pdata,addr = server.recvfrom(buf)
            if not pdata:
                break
            f.write(pdata)
            shutil.copy('gelendosya.txt', 'c:/Users/Enes TEKIN/Desktop/dizin')
            print('Tamamlandı')
            print('Bağlantı kapatılıyor')
            sys.exit()
            

    elif (cmd[:3] == 'GET'):

        dosya = cmd[4:]
        os.chdir('c:/Users/Enes TEKIN/Desktop/dizin')
        dosyalar = os.listdir('c:/Users/Enes TEKIN/Desktop/dizin') #göndereceğimiz dosyanın yolunu giriyoruz

        if dosya in dosyalar:
            f = open(dosya , 'rb')
            l = f.read(buf)
            while (l):
                server.sendto(l,addr)
                print('Gönderiliyor\n ',repr(l))
                l = f.read(buf)
                print('Tamamlandı')
                print('Bağlantı kapatılıyor')
                sys.exit()

        else:
            print('Dosya dizinde mevcut değil\n')
            sys.exit()
            print('Bağlantı kapatılıyor')
            