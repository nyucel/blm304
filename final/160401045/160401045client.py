#Gökçe Kuler
import socket
import time 
import os

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ipadresi=input("Lütfen bağlanmak istediğiniz adresi giriniz")
server_address = (ipadresi, 142)
print('{} port {}'.format(*server_address))
mesaj=b'baglanti kuruluyor'          
sock.connect(server_address)
simdikizaman=int(round(time.time()*1000)) #sunucu ile veri gönderimi başlatılmadan önceki zaman
sock.send(mesaj)
data = sock.recv(1024)
istekzamani=int(round(time.time()*1000)) #sunucudan cevap geldikten sonraki zaman
gecikenzaman=istekzamani-simdikizaman
ekleneceksure=(gecikenzaman/1000)/2 
data=int(data)+ekleneceksure
b=(time.localtime(int(data)/1000))  #bulunan sürenin tarih ve saate dönüştürülmesi
yil=b.tm_year
ay=b.tm_mon
gun=b.tm_mday
saat=b.tm_hour
dakika=b.tm_min
saniye=b.tm_sec
if(len(str(ay))==1):
    ay="0"+str(ay)
if(len(str(gun))==1):
    gun="0"+str(gun)
if(len(str(saat))==1):
    saat="0"+str(saat)
if(len(str(dakika))==1):
    dakika="0"+str(dakika)
if(len(str(saniye)) ==1 ):
    saniye="0" + str(saniye)
komut="date -s" +" " +  '" '+ str(ay)+ "/" + str(gun) + "/" + str(yil) + " " + str(saat) + ":" + str(dakika) + ":" + str(saniye) + '"'
print(komut)

os.system(komut) #bilgisayarın zamanını günceller
print('program sonlandı')
sock.close()  

