# Nurşah Koç 130401055
import socket
import os
import sys


def Listeleme():
    print("Alindi bilgisi gonderiliyor.")
    mesaj = "Listeleme komutu alindi."
    mesajE = mesaj.encode('utf-8')
    s.sendto(mesajE, clientAddr)
    print("Mesaj istemciye yollandi.")
    print("Dizindeki dosyalar listeleniyor.")

    F = os.listdir(
        path="/var/games/130401055/server") # dizin kismi degistirilmeli

    Liste = []
    for file in F:
        Liste.append(file)
    ListeS = str(Liste)
    ListeE = ListeS.encode('utf-8')
    s.sendto(ListeE, clientAddr)
    print("Liste sunucudan yollandi.")


def GetKomutu(j):
    print("Alindi bilgisi gonderiliyor.")
    mesaj = "Alinan get komutu isleniyor."
    mesajE = mesaj.encode('utf-8')
    s.sendto(mesajE, clientAddr)
    print("Mesaj istemciye yollandi.")

    if os.path.isfile(j):
        mesaj = "Dosya dizinde mevcut."
        mesajE = mesaj.encode('utf-8')
        s.sendto(mesajE, clientAddr)
        print("Dosya mevcut bilgisi paylasildi.")

        i = 0
        boyut = os.stat(j)
        paketS = boyut.st_size
        print("Dosya boyutu(bytes):" + str(paketS))
        paketN = int(paketS / 4096)
        paketN = paketN + 1
        paketNS = str(paketN)
        paketNE = paketNS.encode('utf8')
        s.sendto(paketNE, clientAddr)

        countD = int(paketN)
        Dosyab = open(j, "rb")
        while countD != 0:
            Dosyac = Dosyab.read(4096)
            s.sendto(Dosyac, clientAddr)
            i += 1
            countD -= 1
            print("Paket numarasi:" + str(i))
            print("Veri gonderimi devam ediyor:")
        Dosyab.close()
        print("GET fonksiyonu ile sunucudan dosya yollandi")

    else:
        mesaj = "Hata: Belirtilen dosya sunucu dizininde yok."
        mesajE = mesaj.encode('utf-8')
        s.sendto(mesajE, clientAddr)
        print("Mesaj yollandi.")


def PutKomutu():
    print("Alindi bilgisi gonderiliyor.")
    mesaj = "Put komutu alindi."
    mesajE = mesaj.encode('utf-8')
    s.sendto(mesajE, clientAddr)
    print("Mesaj istemciye yollandi.")

    if islem[0] == "PUT":

        Dosya = open(islem[1], "wb")
        print("Belirtilen dosya varsa paket alimi baslayacak.")
        try:
            Count, countaddress = s.recvfrom(4096)
        except:
            print("Bir hata olustu.")
            sys.exit()

        CountD = Count.decode('utf8')
        CountD = int(CountD)

        while CountD != 0:
            ServerData, serverAddr = s.recvfrom(4096)
            CountD -= 1

        Dosya.close()
        print("Yeni dosya alindi. Dizin icerigini kontrol edin.")


def CikisYap():
    print(
        "Sistem cikis yapacak. Ancak bu istemciye bildirilmeyecek.")
    s.close()
    sys.exit()


def HataliKomut():
    mesaj = "Hata: Sunucu " + \
        islem[0] + " komutunu anlayamadi."
    mesajE = mesaj.encode('utf-8')
    s.sendto(mesajE, clientAddr)
    print("Hatali komut mesaji gonderildi.")


host = ""
port = 42

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Sunucu soketi baslatildi.")
    s.bind((host, port))
    print("Binding basarili. Istemci bekleniyor.")
except socket.error:
    print("Soket olusturma basarisiz.")
    sys.exit()

while True:
    try:
        veri, clientAddr = s.recvfrom(4096)
    except ConnectionResetError:
        print(
            "Hata. Port numaralari eslesmiyor.")
        sys.exit()
    veriA = veri.decode('utf8')
    islem = veriA.split()
    if islem[0] == "ls":
        print("ls isleme alindi")
        Listeleme()
    elif islem[0] == "GET":
        print("GET isleme alindi")
        GetKomutu(islem[1])
    elif islem[0] == "PUT":
        print("PUT isleme alindi")
        PutKomutu()
    elif islem[0] == "exit":
        print("exit isleme alindi")
        CikisYap()
    else:
        HataliKomut()

print("Programdan cikilacak. ")
quit()
