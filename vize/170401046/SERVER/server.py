# 170401046 Oguz Kaya

import socket
import os
import sys

IP = "127.0.0.1"
Port = 42
Sunucu_skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
Sunucu_skt.bind((IP, Port))

def DosyaListele():
    D = os.listdir()
    Dosyalar = str(D).encode('utf-8')
    Sunucu_skt.sendto(Dosyalar, istemci_adresi)

while True:
    secim, istemci_adresi = Sunucu_skt.recvfrom(4096)
    secim = secim.decode('utf8')
    list_sec = secim.split()
    if list_sec[0] == "list":
        DosyaListele()

    elif list_sec[0] == "exit":
        Sunucu_skt.close()
        sys.exit()

    elif list_sec[0] == "put":
        dosya_adi = list_sec[1]
        f = open(dosya_adi, "wb")
        veri = Sunucu_skt.recvfrom(4096)
        try:
            while veri:
                veri = Sunucu_skt.recvfrom(4096)
                f.write(veri)
        except socket.timeout:
            f.close()

    elif list_sec[0] == "get":
        dosya = list_sec[1]
        f = open(dosya, "rb")
        dosya_adi = dosya.encode('utf-8')
        Sunucu_skt.sendto(dosya_adi, istemci_adresi)
        veri = f.read(4096)
        Sunucu_skt.sendto(veri, istemci_adresi)
        while veri:
            if Sunucu_skt.sendto(veri, istemci_adresi):
                veri = f.read(4096)
        f.close()
