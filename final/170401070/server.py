#170401070-Başak KILIÇ

import socket 
from datetime import datetime, timedelta
from os import sys
import time
import pytz
import datetime

d_ip = input("Sunucunun adresi: ")
port = 142
utc = +2
def zaman_formati(zaman):
	tarih = str( zaman.strftime("%d %B %Y ") )
	zaman = str( datetime.datetime.time(zaman) )

	return ( tarih+zaman )
	

def gecikme_suresi(baglanti):
      	baslangic_zamani = datetime.datetime.now(tz=pytz.utc) + timedelta(hours = utc)
      	z= zaman_formati(baslangic_zamani)	
      	 
      	baglanti.send(bytes(z, encoding='utf-8'))	#Serverdaki saat bilgisi cliente gönderilir.
      	kontrol = baglanti.recv(2048)
      
      	aktarim_zamani = datetime.datetime.now(tz=pytz.utc) + timedelta(hours = utc)	#Gönderim işlemi gerçekleştikten sonraki saat hesaplanır.
      	sure = (aktarim_zamani - baslangic_zamani) / 2			#Ortaya çıkan gecikme hesaplanır.
      	return sure    	
	
try:
   	sunucuSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   	sunucuSocket.bind((d_ip, port))

except:
	print("Bir öneceki işlemde TIME_WAIT durumunda kaldı. ")
	sys.exit()


sunucuSocket.listen(1)
(baglanti, istemciAdres) = sunucuSocket.accept()

gecikme = gecikme_suresi(baglanti)

zaman = datetime.datetime.now(tz=pytz.utc) + timedelta(hours = utc) + gecikme	#Güncel zaman bilgisi istemciye gönderilir.

z = zaman_formati(zaman)	 
baglanti.send(bytes(z, encoding='utf-8'))

if(utc < 0):
	zamanDilimi = " UTC" + str(utc)
else:
	zamanDilimi = " UTC+" + str(utc)
	
baglanti.send(bytes(zamanDilimi, encoding='utf-8'))	#Zaman dilimi istemciye gönderilir.

baglanti.close()
sunucuSocket.close()
print("\nTamalandı.")
