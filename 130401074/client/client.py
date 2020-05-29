"""
    ========================= Veri Haberleşmesi Vize Ödevi ========================
    İsim ve Soyisim: Augusto GOMES JUNIOR
    Ögrenci_No: 130401074
"""

#!/usr/bin/env python3
import socket
import sys, time
import os
IP = "127.0.0.1"
PORT = 10020

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print ("=================== HOŞ GELDİNİZ ==================")
print (" ========== UDP Kullanilan FTP Programi =========== \n")
address = input("Host(127.0.0.1): ")

if not address:
    address = IP
port = input("Port(42): ")

if not port:
    port = PORT
    print ("Baglanti kuruluyor... \n")
    time.sleep(1)

print (" - LIST, cwd dosyaları listelir.")
print (" - GET dosyaismi, dosya adını vererek sunucudan dosya indirilir.")
print (" - PUT dosyaimsi, dosyayı sunucuya yüklenir. \n")

def retrieve(path):
    try:
        sock.settimeout(10)
        sock.sendto(bytes(str("get " + path),'utf-8'),(IP,PORT))
        noerr = bool(sock.recv(1024).decode('utf-8'))
        if noerr:
            print("Dosya indiriliyor...")
            data = sock.recv(1024)
            with open(path,'wb') as wfile:
                while data:
                    wfile.write(data)
                    data = sock.recv(1024)
                print("İndirme bitti, dosya indirildi.")
        else:
            print("Doasy bulunamadı.")
    except socket.timeout:
            print("İndirme bitti, dosya indirildi.")
            sock.settimeout(None)
    except Exception as e:
            print(str(e))

def store(path):
    try:
        rfile = open(path,'rb')
        data = rfile.read(1024)
        print("Dosya yükleniyor...")
        while data:
            sock.sendto(data, (IP,PORT))
            data = rfile.read(1024)
        sock.settimeout(7)
        print(sock.recv(1024).decode('utf-8'))
    except socket.timeout:
        print("Dosya yüklendi.")
        sock.settimeout(None)
    except FileNotFoundError:
        print("Dosya bulunamadı.")
    except Exception as e:
        print(str(e))

def listele():
    sock.sendto("LIST".encode("utf-8"), (IP, PORT))
    print("Kullanıcı Dizini:")
    data = sock.recv(1024).decode('utf-8')
    if data:
        print(data)
    else:
        print("Dizin bostur.")

listele()

while True:
    try:
        command = input("FTP >>> ")
        if not command:
            print ("Lütfen bir komut giriniz.")
            continue
        inp = command.strip().split()
        com = inp[0].upper()
        if com == "EXIT" :
            sock.close()
            print("Oturum kapıtıldı")
            sys.exit(0)
        if len(inp) == 2:
            path = inp[1]
            if com == "GET":
                retrieve(path)
            elif com =="PUT":

                isf = os.path.isfile(path)
                if isf:
                    sock.sendto(command.encode("utf-8"), (IP, PORT))
                    store(path)
                else: print("Dosya bulunamadı.")
            else:
                print("Yanlış komut girdiniz")
        elif len(inp) == 1:
            com = command.split()[0].upper()
            if com == "LIST":
                sock.sendto("LIST".encode("utf-8"), (IP, PORT))
                print("Dizin listeleniyor:")
                data = sock.recv(1024).decode('utf-8')
                if data:
                    print(data)
                else:
                    print("Dizin bostur.")

            else:
                print("Hata! Uygun parametre girmediniz.")
        else:
            print("Hata! Uygun parametre girmediniz.")
    except KeyboardInterrupt:
        sock.close()
        sys.exit(0)

    except Exception as e:
        print ("Yanlis komut girdiniz, yeniden deneyiniz!")
        print(e)
