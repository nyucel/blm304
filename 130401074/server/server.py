"""
    ========================= Veri Haberleşmesi Vize Ödevi ========================
    İsim ve Soyisim: Augusto GOMES JUNIOR
    Ögrenci_No: 130401074
"""

#!/usr/bin/env python3
import socket
import sys, os, time
IP = "127.0.0.1"
PORT = 10020
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP,PORT))

def close():
    print("Baglanti kesiliyor...")
    sock.close()
    print("Baglanti kesildi.")
    sys.exit()


def list_directory(path):
    try:
        ld = os.listdir(path)
        if len(ld) == 0:
            return None
        else:
           max_length = len(max(ld, key=len))
           hd = '+ %*s | %12s | %12s | %20s | %11s | %15s +' % (max_length, 'İsim', 'Dosya Tipi', 'Dosya Boyutu', 'Eişim Tarih', 'Erişim İzin', 'Kullanıcı/Grup')
           tb = '%s\n%s\n%s\n' % ('*' * len(hd), hd, '*' * len(hd))
           data = str("")
           for i in ld:
                filepath = os.path.join(path, i)
                stat = os.stat(path)
                data += '| %*s | %12s | %12s | %20s | %11s | %15s |\n' % (max_length, i, 'Dizin' if os.path.isdir(filepath) else 'Dosya',
                str(stat.st_size) + 'B', time.strftime('%b %d, %Y %H:%M', time.localtime(stat.st_mtime)),
                oct(stat.st_mode)[-4:], str(stat.st_uid) + '/' + str(stat.st_gid))
           ft = '%s\n' % ('*' * len(hd))
           return tb + data + ft
    except Exception as e:
        return "HATA: "+str(e)
        print(str(e))

def retrieve(path,address):
    try:
        no_error = os.path.isfile(path)
        sock.sendto(bytes(str(no_error),'utf-8'),address)
        if not no_error:
            print("Hata oldu dosya, bulunamadı")
        else:
            with open(path,'rb') as rfile:
                data = rfile.read(1024)
                while data:
                    sock.sendto(data,address)
                    data = rfile.read(1024)
    except Exception as e:
         print(str(e))


def store(path,address):
    try:
        sock.settimeout(10)
        data, address = sock.recvfrom(1024)
        with open(path,'wb') as wfile:
            while data:
                wfile.write(data)
                data, address = sock.recvfrom(1024)
                print("Dosya yükleniyor")
            sock.sendto(bytes(str("Dosya yüklendi"),'utf-8'), address)
    except socket.timeout:
        print("Yüklendi")
        sock.settimeout(None)
    except Exception as e:
        sock.sendto(bytes(str("Hata -" + str(e)),'utf-8'), address)
        print(str(e))
        close()


print("Sunucu çalışmaya başladı.")
while True:
    try:
        data, addr = sock.recvfrom(1024)
        inp = data.strip().split()
        com = inp[0].decode('utf-8').upper()
        print("{} komutu {} den geldi ".format(com,addr))
        if len(inp) == 2:
            path = inp[1].decode('utf-8')
            print(path)
            if com == "PUT":
                store(path,addr)
            elif com == "GET":
                print("get", path)
                isf = os.path.isfile(path)
                if isf: retrieve(path,addr)
                else: print("Dosya bulunamadı.")
            else:
                sock.sendto(bytes(str("Hata  yanlış komut"),'utf-8'), addr)
        elif len(inp) == 1:
            if com == "LIST":
                data = list_directory(os.getcwd())
                if data:
                    sock.sendto(data.encode('utf-8'), addr)
                else: sock.sendto("CWD: Dizin bostur".encode('utf-8'), addr)
            else:
                sock.sendto("Bilinmeyen komut girdiniz".encode('utf-8'), addr)
        print("Yeni komut bekleniyor")
    except KeyboardInterrupt:
        sock.close()
        print("Sunucu durduruldu.")
        sys.exit(0)
    except Exception as ex:
         print(str(ex))
