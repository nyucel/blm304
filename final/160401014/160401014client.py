#Selin KURT 160401014
import socket
import os 
import time

newsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = input("Baglanmak istenilen sunucunun ip adresini giriniz: ")
server_info = (server_ip, 142)
print('{} port {}'.format(*server_info))
mesaj = b"sunucuya baglaniliyor"          
newsocket.connect(server_info)

time_now = int(round(time.time()*1000)) 
newsocket.send(mesaj)

data = newsocket.recv(1024)
time_data =int(round(time.time()*1000)) #sunucudan alınan verinin zamanı
fark = ((time_data-time_now)/1000)/2
data = int(data)+fark
time1 = (time.localtime(int(data)/1000))  
yil = time1.tm_year
ay = time1.tm_mon
gun = time1.tm_mday
saat = time1.tm_hour
dakika = time1.tm_min
saniye = time1.tm_sec

tarih = "date -s" +" " +'" '+ str(ay)+ "/" + str(gun) + "/" + str(yil) + " " + str(saat) + ":" + str(dakika) + ":" + str(saniye) + '" '
print(tarih)

os.system(tarih) 
newsocket.close()  
