#170401011 Berfin Okuducu
import socket
import sys
import os

def list():
    try:
        data, address = client.recvfrom(4096)
        File=data.decode('utf-8')
        print("Dosyalar:")
        print(File)
    except:
        print("Baglanti hatasi")
        sys.exit()

def GET(dosya):
    try:
        data, address = client.recvfrom(4096)
    except:
        print("Baglanti hatasi")
        sys.exit()
    if(data.decode('utf-8')=="Dosya sunucu dizininde bulunamadi"):
        print(data.decode('utf-8'))
    elif(dosya in os.listdir()):
        print("Dosya zaten istemci dizininde mevcut.")
    else:
        f=open(dosya,'wb')
        f.write(data)
        f.close()
        print("Dosya istemci dizinine indirildi.")

def PUT(dosya):
    f=open(dosya,'rb')
    veri=f.read()
    try:
        client.sendto(veri,(host, port))
        sonuc,adress=client.recvfrom(4096)
        sonuc=sonuc.decode('utf-8')
        print(sonuc)
    except:
        print("Baglanti hatasi")



host=input("Baglanilacak sunucunun IP adresini giriniz: ")
port=42
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
   istemci_mesaji="İstemci baglandi"
   istemci_mesaji=istemci_mesaji.encode('utf-8')
   client.sendto(istemci_mesaji,(host, port))
   mesaj,adress=client.recvfrom(4096)
   mesaj=mesaj.decode('utf-8')
   print(str(mesaj))
except:
    print("Baglanti basarisiz.")
    sys.exit()

while True:
    print("İslemler:  List /GET /PUT / -1(Cikis Icin -1 Giriniz )")
    secim = str(input("Yapmak istenilen islem: "))
    istemci_secim = secim.encode('utf-8')
    try:
        client.sendto(istemci_secim, (host, port))
    except:
        print("Baglanti hatasi.")
        sys.exit()

    if(secim=="List"):
        list()

    elif(secim=="GET"):
        dosya=input("Indirilecek dosyanin ismini giriniz: ")
        dosyaadi=dosya.encode('utf-8')
        try:
            client.sendto(dosyaadi,(host, port))
            GET(dosya)
        except:
            print("Baglanti Hatasi")
            sys.exit()

    elif(secim=="PUT"):
        p_dosya=input("Yüklenecek dosyanin ismini giriniz: ")
        p_dosya_adi=p_dosya.encode('utf-8')
        if(p_dosya not in os.listdir()):
            hata="Dosya Yok"
            hata=hata.encode('utf-8')
            try:
                client.sendto(hata, (host, port))
                hata_mesaji, adress = client.recvfrom(4096)
                hata_mesaji = hata_mesaji.decode('utf-8')
                print(str(hata_mesaji))
            except:
                print("Baglanti hatasi")
                sys.exit()
        else:
            try:
                client.sendto(p_dosya_adi, (host, port))
                varmi,adress=client.recvfrom(4096)
                varmi=varmi.decode('utf-8')
                if(varmi=="Dosya zaten sunucu dizininde mevcut."):
                    print(str(varmi))
                else:
                    PUT(p_dosya)
            except:
                print("Bağlanti Hatasi")
                sys.exit()
    elif(secim=="-1"):
        print("Cikis yapiliyor...")
        sys.exit()
    else:
        print("Hatali komut girisi")

