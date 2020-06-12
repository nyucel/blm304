#--Bircan ARSLAN 170401013

import socket,time
from time import sleep
import sys, datetime

sunucu = str(socket.gethostbyname(socket.gethostname()+".local")) # Bulunduğu bilgisayara ait IP adresini otomatik olarak alıyor
port = 142 #Dinlenen port

#--UTC DEĞERİNİ DEĞİŞTİRMEK İÇİN TUTULAN DEĞİŞKEN -->  "girilenutc"
girilenutc = "UTC+03" #UTC değerini değiştirmek istiyorsanız tam sayılar için "UTC-03","UTC+05" formatlarını kullanın.

utcint=int(girilenutc[3:])
#sizeutc1 = len(girilenutc[3:])
#sizeutc2=len(girilenutc)

try: 
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP bağlantısı 
    tcp.bind((sunucu, port))#TCP bağlantısı kuruldu
except:
    print("Hata! Sunucu bağlantısı kurulamadı.") #Bağlantı kurulamama kontrolü
    sys.exit()
    
tcp.listen(5)

print("Bulunduğunuz Server'ın IP Adresi: ", sunucu) #Ip adresini giriş ekranına yazdırıyoruz
print("Bağlantı kuruldu.")

zaman = time.time()
baslangic = datetime.datetime.fromtimestamp(zaman).strftime('%Y-%m-%d %H:%M:%S')
print("Şuanki Sistem Saati:", baslangic, "(%s ms)"%str(zaman*1000)[:-5])
defutc = datetime.datetime.now(datetime.timezone.utc).astimezone().tzname() #Sunucunun bulunduğu sistemin utc değerini alıyoruz
test1 = int(time.time())

def gecikme(): #Gecikme hesaplama
    gecikme = int(time.time()-test1)
    return gecikme

def ayni(): 
    mstime = str(time.time()*1000).split('.')
    delay = gecikme()
    senddate = int(mstime[0])+delay
    return senddate
def gerial():
    fark = utcint - int(defutc)
    msutc1 = fark*60*60*1000
    mstime = str(time.time()*1000).split('.')
    delay = gecikme()
    senddate = int(mstime[0])+msutc1+delay
    return senddate
def ilerial():
    fark = utcint - int(defutc)
    msutc1 = fark*60*60*1000
    mstime = str(time.time()*1000).split('.')
    delay = gecikme()
    senddate = int(mstime[0])+msutc1+delay
    return senddate
while True:
    baglanti, adres = tcp.accept() 
    if (int(defutc) == utcint): 
        gonderilecek = ayni()
        baglanti.send(str(gonderilecek).encode())
        baglanti.send(girilenutc.encode())
        print("Sunucun Tarih ve Saat Bilgisi:",datetime.datetime.fromtimestamp(int(gonderilecek)/1000).strftime('%Y-%m-%d %H:%M:%S'),"(%s ms)"%gonderilecek, "Sunucunun Bulunduğu Zaman Dilimi", girilenutc)
    if (utcint < int(defutc)): 
        gonderilecek = gerial()
        baglanti.send(str(gonderilecek).encode())
        baglanti.send(girilenutc.encode())
        print("Sunucunun Tarih ve Saati:",datetime.datetime.fromtimestamp(int(gonderilecek)/1000).strftime('%Y-%m-%d %H:%M:%S'),"(%s ms)"%gonderilecek, "Sunucunun Bulunduğu Zaman Dilimi", girilenutc)
    if (utcint > int(defutc)):
        gonderilecek = ilerial()
        baglanti.send(str(gonderilecek).encode())
        baglanti.send(girilenutc.encode())
        print("Sunucunun Tarih ve Saat Bilgisi:",datetime.datetime.fromtimestamp(int(gonderilecek)/1000).strftime('%Y-%m-%d %H:%M:%S'),"(%s ms)"%gonderilecek, "Sunucunun Bulunduğu Zaman Dilimi", girilenutc)
