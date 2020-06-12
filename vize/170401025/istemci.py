import socket
import sys
import os

#Eda Defterli / 170401025
def listele():
    try:
        veri, adres = client.recvfrom(4096)
        dosya=veri.decode('utf-8')
        print("Dosyalar:")
        print(dosya)
    except:
        print("Baglanti hatasi olustu.")
        sys.exit()

def GET(dosya):
    try:
        veri, adres = client.recvfrom(4096)
    except:
        print("Baglanti hatasi")
        sys.exit()
    if(veri.decode('utf-8')=="Dosya bulunamadi"):
        print(veri.decode('utf-8'))
    elif(dosya in os.listdir()):
        print("Dosya zaten istemci dizininde mevcut.")
    else:
        f=open(dosya,'wb')
        f.write(veri)
        f.close()
        print("indirildi.")

def PUT(dosya):
    if(dosya in os.listdir()):
        f=open(dosya,'rb')
        veri=f.read()
        try:
            client.sendto(veri,(host, port))
            sonuc,adress=client.recvfrom(4096)
            sonuc=sonuc.decode('utf-8')
            print(sonuc)
        except:
            print("Baglanti hatasi")
    else:
        print("Gönderilecek dosya istemci dizininde bulunamadi")


host=input("Baglanilacak sunucunun IP adresini giriniz: ")
port=42

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except:
    print("Baglanti basarisiz.")
    sys.exit()

while True:
    print("İslemler:  List /GET /PUT / -1(Cikis Icin -1 Giriniz )")
    secim = str(input("Yapmak istediginiz islemi secin: "))
    secim1 = secim.encode('utf-8')
    client.sendto(secim1, (host, port))

    if(secim=="List"):
        print("Dosyalar listeleniyor...")
        listele()

    elif(secim=="GET"):
        dosya=input("Indirilecek dosyanin ismini giriniz: ")
        dosyaadi=dosya.encode('utf-8')
        client.sendto(dosyaadi,(host, port))
        GET(dosya)

    elif(secim=="PUT"):
        p_dosya=input("Yüklenecek dosyanin ismini giriniz: ")
        p_dosya_adi=p_dosya.encode('utf-8')
        client.sendto(p_dosya_adi, (host, port))
        kontrol,adres=client.recvfrom(4096)
        kontrol=kontrol.decode('utf-8')
        if(kontrol=="Dosya zaten sunucu dizininde mevcut."):
            print(str(kontrol))
        else:
            PUT(p_dosya)
    elif(secim=="-1"):
        print("Cikis yapiliyor...")
        sys.exit()
    else:
        print("Hatali komut girisi")
