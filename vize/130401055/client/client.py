# Nurşah Koç 130401055
import socket
import os
import sys


host = sys.argv[1]
# host =  [buraya sunucu IP yazilarak ustteki satir yoruma donusturulebilir.]
port = 42

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Istemci soketi baslatildi.")
    s.setblocking(0)
    s.settimeout(15)
except socket.error:
    print("Soket olusturma basarisiz.")
    sys.exit()


while True:
    komut = input(
        "\nLutfen komut belirtiniz: \na. ls\nb. GET dosya_adi\nc. PUT dosya_adi\nd. exit\n ")

    KomutE = komut.encode('utf-8')
    s.sendto(KomutE, (host, port))
    KomutA = komut.split()

    if KomutA[0] == "ls":
        print("Alindi bilgisi kontrol ediliyor.")
        try:
            ClientData, clientAddr = s.recvfrom(51200)
        except:
            print("Bir hata olustu.")
            sys.exit()

        text = ClientData.decode('utf8')
        print(text)

        if text == "Listeleme komutu alindi.":
            ClientDataB, clientAddrB = s.recvfrom(4096)
            text2 = ClientDataB.decode('utf8')
            print(text2)
        else:
            print("Hata.")

    elif KomutA[0] == "GET":
        print("Alindi bilgisi kontrol ediliyor.")
        try:
            ClientData, clientAddr = s.recvfrom(51200)
        except:
            print("Bir hata olustu.")
            sys.exit()
        text = ClientData.decode('utf8')
        print(text)

        try:
            ClientData2, clientAddr2 = s.recvfrom(51200)
        except:
            print("Bir hata olustu.")
            sys.exit()

        text2 = ClientData2.decode('utf8')
        print(text2)

        if len(text2) < 30:
            if KomutA[0] == "GET":
                Dosya = open("Alinan-" + KomutA[1], "wb")
                d = 0
                try:
                    CountP, countaddress = s.recvfrom(4096)
                except:
                    print("Bir hata olustu.")
                    sys.exit()

                PaketC = CountP.decode('utf8')
                PaketC2 = int(PaketC)
                print("Dizinde dosya varsa paketler alinmaya baslayacak.")
                while PaketC2 != 0:
                    ClientbData, clientbAddr = s.recvfrom(4096)
                    dataS = Dosya.write(ClientbData)
                    d += 1
                    print("Alinan paket numarasi:" + str(d))
                    PaketC2 -= 1

                Dosya.close()
                print(
                    "Yeni dosya alindi. Dizin icerigini kontrol edin.")

    elif KomutA[0] == "PUT":
        print("Alindi bilgisi kontrol ediliyor.")
        try:
            ClientData, clientAddr = s.recvfrom(4096)
        except:
            print("Bir hata olustu.")
            sys.exit()

        text = ClientData.decode('utf8')
        print(text)
        print("Veri gonderilmeye baslaniyor.")

        if text == "Put komutu alindi.":
            if os.path.isfile(KomutA[1]):

                i = 0
                boyut = os.stat(KomutA[1])
                paketS = boyut.st_size
                print("Dosya boyutu(bytes):" + str(paketS))
                paketN = int(paketS / 4096)
                paketN = paketN + 1
                print("Gonderilecek paket sayisi: " + str(paketN))
                paketSt = str(paketN)
                paketE = paketSt.encode('utf8')
                s.sendto(paketE, clientAddr)
                paketI = int(paketN)
                Dosyad = open(KomutA[1], "rb")

                while paketI != 0:
                    Run = Dosyad.read(4096)
                    s.sendto(Run, clientAddr)
                    i += 1
                    paketI -= 1
                    print("Paket numarasi:" + str(i))
                    print("Veri gonderimi devam ediyor:")

                Dosyad.close()

                print("PUT fonksiyonu ile istemciden dosya yollandi")
            else:
                print("Hata: Belirtilen dosya client.py dizininde yok.")
        else:
            print("Gecersiz")

    elif KomutA[0] == "exit":
        print(
            "Sunucu cikis yapsa da bununla ilgili bildirim almayacaksiniz.")

    else:
        try:
            ClientData, clientAddr = s.recvfrom(51200)
        except:
            print("Bir hata olustu.")
            sys.exit()
        text = ClientData.decode('utf8')
        print(text)

print("Programdan cikilacak. ")  # bu calistirilmayacak
quit()
