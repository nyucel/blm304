# 170401046 Oguz Kaya

import socket
import sys

host = str(input("Server ip giriniz : "))
port = 42
istemci_skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    secim = input("1. list\n2. put [dosya_adi]\n3. get [dosya_adi]\n4. exit\nSeciminizi giriniz :  ")
    ist_sec = secim.encode('utf-8')
    istemci_skt.sendto(ist_sec, (host, port))
    a = secim.split()
    if a[0] == "list":
        dosyalar = istemci_skt.recvfrom(4096)
        metin = dosyalar[0]
        print(metin)

    elif a[0] == "exit":
        istemci_skt.close()
        sys.exit()

    elif a[0] == "put":
        dosya = a[1]
        f = open(dosya, "rb")
        veri = f.read(4096)
        while veri:
            istemci_skt.sendto(veri, (host, port))
            veri = f.read(4096)
        f.close()

    elif a[0] == "get":
        dosya_adi = istemci_skt.recvfrom(4096)[0]
        dosya_adi = dosya_adi.decode('utf-8')
        f = open(dosya_adi, "wb")
        veri = istemci_skt.recvfrom(4096)
        try:
            while veri:
                veri = istemci_skt.recvfrom(4096)
                f.write(veri)
        except socket.timeout:
            f.close()


