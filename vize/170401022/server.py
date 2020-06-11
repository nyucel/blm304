#170401022 Cihan PAR
import socket
from os import listdir

def listeleme():
    print("Server: Dosyalar görüntüleniyor.")
    dosyalar = "------------------------\n"
    for i in listdir():
        dosyalar += i+"\n"
    return dosyalar

def veriyolla(veri, adres):
    try:
        serverudp.sendto(veri.encode("utf-8"),adres)
    except:
        print("Bağlantı Hatası!")

def verial():
    try:
        alinanveri, adres=serverudp.recvfrom(sizebuffer)
        return alinanveri.decode("utf-8")
    except:
        print("Bağlantı Hatası!")

serveripaddress = input(" Server Adres: ")
serverport = 42
serverudp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverudp.bind((serveripaddress, serverport))
sizebuffer = 4096

try: 
    print("Server: Istem bekleniyor.")
    data, address = serverudp.recvfrom(sizebuffer)
    veriyolla("Server : Bağlantı kuruldu.",address)
    print("Server : Bağlantı kuruldu.")
except:
    print("Server : Bağlantı hatası.")


while True:    
    print("Server : Komut bekleniyor.")
    veriyolla("Server : Komut bekleniyor.",address)
        
    data = verial()                      #komut kodu gelecek.                     
    print("Server: Komut: \t "+data)

    if data=="GET":
        dosyalar=listeleme()
        print("Server: Dosya isimleri gönderiliyor...")
        veriyolla(dosyalar,address)                              #dosyalar gönderiliyor
        veriyolla("Server : Komut alındı, dosya ismi bekleniyor",address)
        print("Server : Dosya ismi bekleniyor.")
        dosyaismi=verial()                                          #istenen dosya gelecek
        print("Server: Istenen dosya : "+dosyaismi)
        print("Server: veri gönderiliyor...")
        dosya = open(dosyaismi.encode(), "rb").read()
        serverudp.sendto(dosya,address)
        veriyolla("Server : Dosya Gönderildi",address)
    elif (data=="PUT"):
        print("Server: Dosya aktarılıyor.")
        alinandosyaismi = verial()
        alinacakdosya, address = serverudp.recvfrom(sizebuffer)
        with open(alinandosyaismi.encode(),"wb") as dosya:
            dosya.write(alinacakdosya)
            dosya.close()
        veriyolla("Server : Dosya yazıldı.",address)
    else:
        print("Server: Hatalı komut!")
