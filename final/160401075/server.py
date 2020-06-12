#Batuhan METİN
#160401075

import socket 
from datetime import datetime, timedelta
from os import sys
import time
import pytz
import datetime

aa_ip = input("Sunucunun adresi: ")
port = 142
utc = +2
def forZaman(zaman):
	tarih = str( zaman.strftime("%d %B %Y ") )
	zaman = str( datetime.datetime.time(zaman) )

	return ( tarih+zaman )
	

def gecikmeSuresi(baglanti):
      	baslangic_zamani = datetime.datetime.now(tz=pytz.utc) + timedelta(hours = utc)
      	z= forZaman(baslangic_zamani)	
      	 
      	baglanti.send(bytes(z, encoding='utf-8'))	
      	kontrol = baglanti.recv(2048)
      
      	aktarim_zamani = datetime.datetime.now(tz=pytz.utc) + timedelta(hours = utc)	
      	sure = (aktarim_zamani - baslangic_zamani) / 2			
      	return sure    	
	
try:
   	socketSunucu = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   	socketSunucu.bind((aa_ip, port))

except:
	print("TIME_WAIT durumunda kaldı. ")
	sys.exit()


socketSunucu.listen(1)
(baglanti, istemciAdres) = socketSunucu.accept()

gecikme = gecikmeSuresi(baglanti)

zaman = datetime.datetime.now(tz=pytz.utc) + timedelta(hours = utc) + gecikme	

z = forZaman(zaman)	 
baglanti.send(bytes(z, encoding='utf-8'))

if(utc < 0):
	dil_Zaman = " UTC" + str(utc)
else:
	dil_Zaman = " UTC+" + str(utc)
	
baglanti.send(bytes(dil_Zaman, encoding='utf-8'))	

baglanti.close()
socketSunucu.close()
print("\nBitiş.")
