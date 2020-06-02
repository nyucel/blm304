#!/usr/bin/env python3

#Fahrettin Orkun İncili - 150401013

import socket
from scapy.all import*


IP=input("IP:")
PORT = 42
print("""
############################################################
|                                                          |
|  l            komutu sunucudaki dosyaları listeler       |
| get           komutundan sonra dosya adı girilmelidir    |
| put           komutundan sonra dosya adı girilmelidir    |
| exit          çıkış                                      |
############################################################

""")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((IP, PORT))
    while True:
        choice = input("Yapacağınız işlemi seçiniz:")
        byte_choice = str.encode(choice)

        s.sendall(byte_choice)

        if choice=="l":

            data = s.recv(1024)
            data=data.decode("utf-8")

            print('İndirilebilecek dosyalar: ', data)

        elif choice=="get":

            get=input("Dosya adını giriniz:")
            get=str.encode(get)
            s.sendall(get)

            data = s.recv(1024)
            data = data.decode("utf-8")
            file=open("deneme.txt", "w")
            file.write(data)
            print("Başarılı.Dosya yolu:",os.getcwd()+"/files")


        elif choice=="put":
            current_dir = os.getcwd()
            file_names = os.listdir(current_dir)
            print("Yükleyebileceğiniz dosyalar:",file_names)
            put = input("Dosya adını giriniz:")
            file=open("deneme.txt","r")
            file=file.read()

            put = str.encode(file)
            s.sendall(put)
            print("dosya başarıyla yüklendi")

        elif choice=="exit":
            sys.exit(0)