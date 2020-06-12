#!/usr/bin/python3
# Ahmet Faruk Albayrak - 170401001

"""
Bir ağ zaman sunucusu ve istemcisini aşağıdaki gerekliliklere uygun bir şekilde
yazmalısınız.
◦ Sunucu TCP port 142 kullanmalıdır.
◦ Sunucu kaynak IP adresi ve portu her ne olursa olsun bütün isteklere cevap olarak
zamanı milisaniye cinsinden ve zaman dilimini
(UTC+2 veya UTC-3 gibi)
döndürmelidir.
◦ Zaman dilimi sunucu dosyasının içindeki bir değişken ile değiştirilebilmelidir.
◦ Sunucu yazılımı üzerinde koştuğu işletim sisteminn zaman bilgisini kullanmalıdır.
◦ Kontrol sırasında istemci bilgisayar üzerinde bütün portlar kapatılmış durumda olacaktır.
◦ İstemci bilgisayar üzerinde istemci yazılımı çalıştırıldığında aldığı yanıta göre
bilgisayarın saati ayarlanmalıdır. (70 puan)
◦ İstemci bilgisayar sunucu ile arasında veri gönderip alırken yaşanan gecikmeyi hesaba
katmalı ve sistem saatini buna göre ayarlamalıdır. (20 puan)
• ogrenci_numaranız isimli dizinin içinde README.md isimli bir dosyada yazılımınızın nasıl
yapılandırılacağı ve kullanılacağı yazılmalıdır. (10 puan)
"""

import socket
import time
import datetime

HOST = '0.0.0.0'        # TODO: bunu localhost yapmayi dene
PORT = 142

print("Zaman dilimi UTC+? seklinde tanimlanmistir. Sadece [0,23] araligindaki tamsayilar kabul edilmistir. Ornegin, UTC-3 belirtmek istiyorsaniz 24-3, yani 21 girmelisiniz.")
a = input("Zaman dilimi tamsayisini giriniz(Ornek girdiler: 0, 3, 16, 23): ")
zaman_dilimi = a                                 # zaman_dilimini burdaki a tamsayisini degistirerek degistirebilirisiniz.
TZ = "UTC+" + zaman_dilimi                       # gonderilecek UTC+X stringi

kill_flag = input("Sunucunun ilk gelen baglantiya cevap verdikten sonra kapanmasini istiyor musunuz?(e/h): ")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # tcp socket objemiz: s
s.bind((HOST, PORT))                                    # socketi adresimize bagliyoruz
time.sleep(.5)                                          # bu gecikme objenin duzgun olusmasi icin
s.listen()                                              # socket dinlemeye basliyor
print("Sunucu dinlemede...")

while True:
    istemci_soketi, istemci_adresi = s.accept()                  # client baglantisini kabul ediyoruz ve bize gonderdigi yeni soketi ve istemci ipv4 adresini kaydediyoruz.
    time.sleep(.3)                                               # bu gecikme objenin duzgun olusmasi icin
    print(istemci_adresi, " baglandi.")
    baslangic_isareti = istemci_soketi.recv(1024)                # Istemciden herhangi bir veri geldigi anda basliyoruz ki istemci de gecikmeyi saymaya baslasin.
    gonderilecek_zaman=int(time.time()*1000)                     # ms birimine kadar hassasiyet gonderilen saatin zaman dilimi UTC+0, 1970 epoch tan beri gecen zaman
    istemci_soketi.send(str(gonderilecek_zaman).encode())        # ms olarak gonderdik
    #time.sleep(.5)                                              # bu gecikme time zone u ayri gondermek icin
    istemci_soketi.send(TZ.encode())                             # zaman dilimini de ardindan gonderdik
    istemci_soketi.close()
    if kill_flag == 'e':
        s.close()  # serveri kapat
        break
