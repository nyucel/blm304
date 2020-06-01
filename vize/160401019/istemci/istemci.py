import socket
import sys
import time
import os
import select
#160401019
#Sena Günay

def dosyalari_listele():
    try:
        istemci_veri, istemci_adres = client.recvfrom(4096)
    except ConnectionResetError:
        print("Port Hatasi.")
        sys.exit()
    except:
        print("Zaman asimi veya diger.")
        sys.exit()
    liste = istemci_veri.decode('utf8')
    print(liste)

def GET(indirilecek_dosya):
    try:
        veri, address = client.recvfrom(4096)
    except:
        print("Dosya sunucudan alinamadi.")
        sys.exit()
    dosya=open(indirilecek_dosya,'wb')
    dosya.write(veri)
    dosya.close()
    print("Dosya basariyla indirildi.")

def PUT(gonderilecek_dosya):
    if(gonderilecek_dosya in os.listdir()):
        dosya=open(gonderilecek_dosya,'rb')
        dosya2 = dosya.read()
        try:
            client.sendto(dosya2,(host, port))
        except:
            print("Dosya sunucuya ulasmadi")
    else:
        print("Bu isimde bir dosyaya sahip degilsiniz. ")
        sys.exit()


# Bağlanılacak adres ve port
host = input("Baglanmak istediginiz IP adresini giriniz: ")
port = 4242

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Istemci ile sunucunun baglandiginin kontrolu icin bir mesaj gonderiyoruz
istemci_mesaj = ('istemci baglandi').encode('utf-8')
client.sendto(istemci_mesaj, (host,port))

#Sunucudan baglantinin basarili olduguna dair mesaj alıyor ve
#islem yapılabilecek dosyaları listeliyoruz
data, addr = client.recvfrom(4096)
print("SUNUCUNUN MESAJI: ")
print(str(data))
dosyalari_listele()

islem_alimi= input("Dosya indirmek icin GET,\nDosya yuklemek icin PUT,\nCikis yapmak icin Q yazınız: ")
islem = (islem_alimi).encode('utf-8')
client.sendto(islem, (host,port))

if(islem_alimi=="GET"):
    dosya = input("Indirilecek dosyanin adini giriniz: ")
    dosyaadi = dosya.encode('utf-8')
    client.sendto(dosyaadi, (host, port))
    GET(dosya)
elif(islem_alimi=="PUT"):
    p_dosya=input("Yüklenecek dosyanin adini giriniz: ")
    p_dosya_adi=p_dosya.encode('utf-8')
    client.sendto(p_dosya_adi, (host, port))
    PUT(p_dosya)
elif(islem_alimi=="Q"):
    client.close()
else:
    print("Yanlis komut girdiniz. Lutfen komutları buyuk harflerle ve dogru yazdiginizden emin olun")


