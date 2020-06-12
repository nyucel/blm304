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
◦ İstemci bilgisayar sunucu ile arasında ms gönderip alırken yaşanan gecikmeyi hesaba
katmalı ve sistem saatini buna göre ayarlamalıdır. (20 puan)
• ogrenci_numaranız isimli dizinin içinde README.md isimli bir dosyada yazılımınızın nasıl
yapılandırılacağı ve kullanılacağı yazılmalıdır. (10 puan)
"""

import socket
import time 
import os
import datetime

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # tcp socket objemiz: s
sunucu_adresi=input("Sunucu ipv4 adresini giriniz: ")
port = 142
print("Sunucuya baglaniliyor...")
s.connect((sunucu_adresi, port))                        # sunucu baglantisini gerceklestiriyoruz.
one_hour = 3600000                                      # bir saat bu kadar ms

to_send=b'1'                                            # sunucuya 1 gonderip sunucudan saat bilgisi gelene kadar gecen zamani tutacagiz.
t0=int(time.time()*1000)                                # istemci uzerinde zaman tutuyoruz
s.send(to_send)
gelen_ms = s.recv(1024)
gelen_utc_offset = s.recv(1024)
t1=int(time.time()*1000)                                # sunucudan cevap geldikten sonraki zaman
gecen_sure=t1-t0
eklenecek_sure=(gecen_sure/1000)/2 
#print(gelen_ms)
#print(gelen_utc_offset)

# Burda sunucudan gelen ms degerini ve zaman dilimini ayiriyoruz. 
#a = gelen_ms.decode()
#b = a.split('UTC+')[-1]
#ms = a.split('UTC+')[0]
#c = "UTC+" + b
#print("Sunucu zaman dilimi: ", c)
#print("ms:", ms)
#print("b:", b)
#print("eklenecek_sure:", eklenecek_sure)

ms = gelen_ms.decode()
c = gelen_utc_offset.decode()
print("Sunucu zaman dilimi: ", c)
b = (c.split('UTC+')[-1])


# INTERNET DELAY CORRECTION
ms = int(ms) + eklenecek_sure              # burda ms miktarina internet gecikmesini ekledik.


# UTC CORRECTION
TZ_ms_to_be_added = one_hour * int(b)                  # eklenecek TZ milisaniyesi
ms = int(ms) + int(TZ_ms_to_be_added)                  # ms miktarina zaman_diliminin bize belirttigi saat kadar ms ekledik.


ms = float(ms) / 1000.0
#sys.exit()
saat = datetime.datetime.fromtimestamp(ms).strftime('%m/%d/%Y %H:%M:%S.%f')
print(saat)
komut = 'sudo date -s '
komut = komut + '"' + saat + '"'
print(komut + " komutu calistiriliyor.")

os.system(komut) #bilgisayarın zamanını günceller
print('Saatiniz ayarlandi.')
s.close()

