# 170401018 -- Cemre UZUN

import socket
import sys
from datetime import datetime, timedelta

IP = str(socket.gethostbyname(socket.gethostname() + ".local")) #Sunucunun bulunduğu local IP aliyoruz.
print("\n-> Sunucu IP adresi:", IP )
PORT = 142
UTC = int(input("\nUTC giriniz : "))

#Veri gonderip alma islemlerinde gecen sure hesaplanmalidir.Bu fonksiyon bunu amaclar.
def tekYonluGecikmeHesabi(istemci, UTC):
    ilkZaman = datetime.utcnow() + timedelta(hours = UTC)
    istemci.send(bytes(str(ilkZaman), encoding='utf-8')) #mesaj gonderildi.
    print ("\n...Istemciye gidiliyor...")

    kontrolluIslem = istemci.recv(2048)
    print ("\n...Istemciden donuldu...")

    ikinciZaman = datetime.utcnow() + timedelta(hours = UTC)

    tygecikme = (ikinciZaman - ilkZaman) / 2 #gidis donus arasindaki gecikme hesaplandi tek yonlu gecikmeye ihtiyacim oldugundan 2 ye bolundu.
    return tygecikme

#---  --------------------------------- SUNUCU ---------------------------------  ---#

try:
    sunucuS = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Sunucu soketi olusturuldu.IP ve PORT baglanildi.
    sunucuS.bind((IP, PORT))
except:
    print("\n-> HATA!\nSUNUCU OLUSTURULAMADI!\nTekrar deneyiniz") #IP veya PORT baglanirken sorun olustuysa hata mesaji bastirilir.
    sys.exit()

print("\n |............. Sunucu Hazirlandi .............|")
print("\n |.............................................|  \n")

sunucuS.listen(1) #Sunucu baglanti bekliyor.

istemci, istemciAdres = sunucuS.accept()

tygecikme = tekYonluGecikmeHesabi(istemci, UTC) #Tek yonlu gecikme hesaplanmasi

sunucuZamani = datetime.utcnow() + timedelta(hours = UTC) + tygecikme #istemciye gonderecegimiz zaman gecikmenin de eklendigi zaman olmalidir.
print("\n...Zaman istemciye gonderildi...")

istemci.send(bytes(str(sunucuZamani), encoding='utf-8')) #

zamanDilimi = " UTC + " + str(UTC)

istemci.send(bytes(zamanDilimi, encoding='utf-8'))

istemci.close()
sunucuS.close()

print("\n-> Soketler Kapatildi")
