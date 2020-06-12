import socket
import time
from time import sleep,gmtime
import sys
import datetime

serverIP = str(socket.gethostbyname(socket.gethostname()+".local")) #sunucunun mevcut interface'ine ait IP adresi otomatik alınıyor
port = 142
utcdegeri = "UTC+03" #UTC değerini tutan parametre. UTC değerini değiştirmek isterseniz lütfen bu değişkenin değerini (tam sayılar için UTC-03,UTC+05,utc-03,utc+05 formatlarında, küsuratlı sayılar için ise UTC-0345,UTC+0530,utc-0345,utc+0530 formatlarında) değiştiriniz.
try:
    utc=int(utcdegeri[3:])
    lenutc = len(utcdegeri[3:])
    lenutc2=len(utcdegeri)
except ValueError:
    print("Hata: Lütfen girdiğiniz UTC değerini kontrol ediniz.")
    sys.exit()

try: #tcp bağlantısı ile sunucunun başlatılması
    tcp_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_connect.bind((serverIP, port))
except:
    print("Hata: Server başlatılamadı. Lütfen tekrar deneyiniz.") 
    sys.exit()
tcp_connect.listen(5)
print("Server IP Adresi: ", serverIP) #otomatik alınan IP adresi, istemciye kullanıcı tarafından girilmesi için ekrana yazdırılıyor
print("-------------------------------------------------------------------------------")
print("Network Time Protocol Sunucusu Başlatıldı...")
print("-------------------------------------------------------------------------------")

timestamp = time.time()
firsttime = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
print("Başlangıç saati:", firsttime, "(%s ms)"%str(timestamp*1000)[:-5])
timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzname() #sunucu sisteminin varsayılan (Türkiye saatine göre ayarlı (utc +03)) timezone değeri alınıyor
time1 = int(time.time())
while True:
    conn, addr = tcp_connect.accept()
    print("İstemci IP Adresi ve Portu: ",addr)
    if((lenutc) <= 3): #girilen utc değeri tam sayı ise çalışacak kısım 
        if (int(timezone) == utc): #girilen utc değeri varsayılan timezone değerine eşitse
            datms = str(time.time()*1000).split('.')
            diff = int(time.time()-time1) #gecikmenin hesaplanması
            finaldate = int(datms[0])+diff
            dateitr = str(finaldate)
            dateEN = dateitr.encode()
            conn.send(dateEN)
            sleep(0.002)
            utcdegeriEN = utcdegeri.encode()
            conn.send(utcdegeriEN)
            print("Sunucu Tarih ve Saati:",datetime.datetime.fromtimestamp(int(finaldate)/1000).strftime('%Y-%m-%d %H:%M:%S:%f')[:-4],"(%s ms)"%finaldate, "Sunucu Zaman Dilimi", utcdegeri)
        if (utc < int(timezone)):#saat geri alınacaksa çalışacak kısım
            newtz = utc - int(timezone)
            utcms1 = newtz*60*60*1000
            datms = str(time.time()*1000).split('.')
            diff = int(time.time()-time1) #gecikmenin hesaplanması
            finaldate = int(datms[0])+utcms1+diff
            print("Sunucu Tarih ve Saati:",datetime.datetime.fromtimestamp(int(finaldate)/1000).strftime('%Y-%m-%d %H:%M:%S:%f')[:-4],"(%s ms)"%finaldate, "Sunucu Zaman Dilimi", utcdegeri)
            dateitr = str(finaldate)
            dateEN = dateitr.encode()
            conn.send(dateEN)
            sleep(0.002)
            utcdegeriEN = utcdegeri.encode()
            conn.send(utcdegeriEN)
        if (utc > int(timezone)):#saat ileri alınacaksa çalışacak kısım
            newtz = utc - int(timezone)
            utcms1 = newtz*60*60*1000
            datms = str(time.time()*1000).split('.')
            diff = int(time.time()-time1) #gecikmenin hesaplanması
            finaldate = int(datms[0])+utcms1+diff
            print("Sunucu Tarih ve Saati:",datetime.datetime.fromtimestamp(int(finaldate)/1000).strftime('%Y-%m-%d %H:%M:%S:%f')[:-4],"(%s ms)"%finaldate, "Sunucu Zaman Dilimi", utcdegeri)
            dateitr = str(finaldate)
            dateEN = dateitr.encode()
            conn.send(dateEN)
            sleep(0.002)
            utcdegeriEN = utcdegeri.encode()
            conn.send(utcdegeriEN)
    else: #girilen utc değeri küsuratlı ise çalışacak kısım
        futch = int(utcdegeri[3:lenutc2-2])
        futcm = int(utcdegeri[lenutc2-2:])
        if (futch < int(timezone)): #saat geri alınacaksa çalışacak kısım
            newtz = futch - int(timezone)
            if(newtz == -1):#eğer girilen utc ile varsayılan timezone arasında 1 saatten daha az fark varsa çalışacak kısım
                datms = str(time.time()*1000).split('.')
                datetemp = gmtime(int(datms[0])/1000)
                futcmt = 60 - futcm
                utcms2 = futcmt*60*1000
                diff = int(time.time()-time1) #gecikmenin hesaplanması
                finaldate = int(datms[0])-utcms2+diff
            else:
                datms = str(time.time()*1000).split('.')
                datetemp = gmtime(int(datms[0])/1000)
                utcms1 = newtz*60*60*1000
                utcms2 = futcm*60*1000
                diff = int(time.time()-time1) #gecikmenin hesaplanması
                finaldate = int(datms[0])+utcms1-utcms2+diff
            print("Sunucu Tarih ve Saati:",datetime.datetime.fromtimestamp(int(finaldate)/1000).strftime('%Y-%m-%d %H:%M:%S:%f')[:-4],"(%s ms)"%finaldate, "Sunucu Zaman Dilimi", utcdegeri) 
            dateitr = str(finaldate)
            dateEN = dateitr.encode()
            conn.send(dateEN)
            sleep(0.002)
            utcdegeriEN = utcdegeri.encode()
            conn.send(utcdegeriEN)
        else:#saat ileri alınacaksa çalışacak kısım
            newtz = futch - int(timezone)
            datms = str(time.time()*1000).split('.')
            datetemp = gmtime(int(datms[0])/1000)
            utcms1 = newtz*60*60*1000
            utcms2 = futcm*60*1000
            diff = int(time.time()-time1) #gecikmenin hesaplanması
            finaldate = int(datms[0])+utcms1+utcms2+diff
            print("Sunucu Tarih ve Saati:",datetime.datetime.fromtimestamp(int(finaldate)/1000).strftime('%Y-%m-%d %H:%M:%S:%f')[:-4],"(%s ms)"%finaldate, "Sunucu Zaman Dilimi", utcdegeri)
            dateitr = str(finaldate)
            dateEN = dateitr.encode()
            conn.send(dateEN)
            sleep(0.002)
            utcdegeriEN = utcdegeri.encode()
            conn.send(utcdegeriEN)