import socket
from os import system , name
import os
import sys
import struct
import time


#MELİSA BAYRAMLI / 140401052

ip = input("Sunucu IP adresini giriniz: (127.0.0.1) ")
port = 42
BUFFER_SIZE = 4096
serverAddressPort=(ip,port)
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def conn():
    print("Sunucu isteği gönderiliyor..")
    try:
        udp_socket.connect((ip, port))
        print("Bağlanti başarılı..")
    except:
        print("\n Baglanti başarısız tekrar deneyin ")
        return
def list_files():
    print("Dosyalar isteniyor..\n")
    try:
        udp_socket.sendto(bytes("LIST", encoding='utf-8'), serverAddressPort)

        # Send list request

    except:
        print( "Sunucu isteği yapilamadi, baglantidan emin olun....")
        return
    try:
        number_of_files = struct.unpack("i", udp_socket.recv(4))[0]

        for i in range(int(number_of_files)):
            file_name_size = struct.unpack("i", udp_socket.recv(4))[0]
            file_name = udp_socket.recv(file_name_size)
            file_size = struct.unpack("i", udp_socket.recv(4))[0]
            print("\t{} - {}b".format(file_name, file_size))
            udp_socket.send(bytes("1"))
        total_directory_size = struct.unpack("i", udp_socket.recv(4))[0]
        print("Toplam dizin boyutu: {}b".format(total_directory_size))
    except:
        print("Giris alinamadi")
        return
    try:
        udp_socket.send(bytes("1"))
        return
    except:
        print( "Sunucu onayi alinamadi...")
        return



def put(file_name):  # dosya yükleme
    udp_socket.sendto(bytes("PUT",encoding='utf-8'),serverAddressPort)
    time.sleep(1)
    if(os.path.exists(file_name)==True):
        udp_socket.sendto(bytes("bulundu",encoding='utf-8'),serverAddressPort)
        time.sleep(1)
        udp_socket.sendto(bytes(file_name,encoding='utf-8'),serverAddressPort)
        time.sleep(1)
        content=open(file_name,"rb")
        l=content.read(BUFFER_SIZE)
        content.close()
        udp_socket.sendto(l,serverAddressPort)
        kontrol = udp_socket.recvfrom(4096)
        if(kontrol[0].decode("utf-8")=="OK"):
            print("\n** PUT: Dosya basariyla sunucuya yuklenmistir...")
        else:
            print('\nSunucu icerisinde zaten "', file_name, '" adinda bir dosya var')
            iptal=input("İptal için 1 girin:")
            if(iptal==1):
                print("Dosya yüklenilmesi iptal edildi.")
            else:
                print("Basriyla gerçekleştirildi... ")

    else:        # PUT yapilacak dosya istemcide bulunmuyorsa
        print("\n!! Girdiginiz adda bir dosya istemcide bulunamadi..")
        udp_socket.sendto(bytes("bulunamadi", encoding='utf-8'), serverAddressPort) # Bulunamadigini sunucuya bildirir


def get(file_name):  # dosya indirme
    udp_socket.sendto(bytes("GET",encoding='utf-8'),serverAddressPort)
    time.sleep(1)
    udp_socket.sendto(bytes(file_name, encoding='utf-8'), serverAddressPort)
    time.sleep(1)
    iptal = 0
    kontrol = udp_socket.recvfrom(4096)  # GET yapilacak dosyanin istemcide olup olmamasi kontrolu

    if (kontrol[0].decode("utf-8") == "thereis"):  # Dosya istemcide bulunuyorsa
        data, addr = udp_socket.recvfrom(4096)

        iptal = upload(file_name, data)
        if (iptal == 0):  # GET islemi iptal edilmezse sunucuya bunu bildirir
            udp_socket.sendto(bytes("iptal degil", encoding='utf-8'), serverAddressPort)
            print("\n** GET: Dosya basariyla istemciye yuklenmistir...")
    else:  # Dosya istemcide bulunmuyorsa
        print("\n!! Girdiginiz adda bir dosya sunucuda bulunamadi..")
    if (iptal == 1):  # GET islemi iptal edilirse
        udp_socket.sendto(bytes("iptal", encoding='utf-8'), serverAddressPort)
        print("\n!! Dosyanin istemciye yuklenmesi IPTAL edildi..")


def upload(file_name,data):
    if(os.path.exists(file_name)==True):
        print('"\nİstemcide var "',file_name,'"adinda dosya bulunmaktadır.')

    else:
        file=open(file_name,"wb")
        file.write(data)
        file.close()
    return  0

def quit():
    komut = "QUIT".encode()
    udp_socket.send(komut)
    
    udp_socket.close()
    print("Server bağlantısı sonlandırılıyor.. ")
    return

print ("\n \n FTP istemciye hoş geldiniz. \nAşağıdaki işlevlerden birini arayın: \nCONN: Sunucuya bağlan \nPUT dosya_yolu: Dosya yükle \n LIST: Dosyaları listele \n GET dosya_yolu: Dosya indir \ nQUIT: Çıkış" )

while True:

    komut = input("Komut giriniz: ")
    if(komut=="CONN"):
        print("\n")
        conn()
    elif (komut == "LIST"):
        print("\n")
        list_files()

    elif (komut == "PUT"):
        file_name= input("\nPUT islemi icin dosya adini giriniz: ")

        udp_socket.settimeout(5)
        try:
            put(file_name)
        except:  # PUT islemi 5 saniye icerisinde gerceklesmezse
            print("\n!!!\nHATA: Sunucu ile baglanti koptu ..\nDosya sunucuya yüklenemedi. Tekrar deneyiniz..")
            quit()
            break

    elif (komut== "GET"):
        dosyaAd = input("\nGET islemi icin dosya adını giriniz: ")

        udp_socket.settimeout(5)
        try:
            get(dosyaAd)
        except:  # GET islemi 5 saniye icerisinde gerceklesmezse

            print("\n!!!\nHATA: Sunucu ile baglanti koptu..\nDosya istemciye yüklenemedi. Tekrar deneyiniz..")
            quit()
            break

    elif (komut=="QUIT"):
        quit()
        break
    else:
        print("\nYanlis komut girdiniz.. Tekrar deneyiniz..\n\n")