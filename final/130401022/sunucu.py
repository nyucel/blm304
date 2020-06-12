import socket
import time
from datetime import datetime
import os,sys
import win32api

#HASAN SESLİ                        #Hasan SESLİ

BUFFER_BOYUTU = 1024  
UTC=+9   #utc bilgisi burdan integer olarak değiştirilebilir
sunucu_UTC = int(time.strftime('%z'))
print("\nUTC degeri : ",UTC," Sunucu UTC degeri : ",int(sunucu_UTC/100))
sunucu_UTC=int(sunucu_UTC/100)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 142)) #localhost ip ve 142 portu dinliyor
s.listen(1)
conn, addr = s.accept()

print ('\nBağlanan adres ve port numarası: ', addr)
data = conn.recv(BUFFER_BOYUTU)
mesaj = data.decode('utf8')
print ("\nreceived data:", mesaj)


milliseconds = int(round(time.time() * 1000))
istenen_utc = UTC - sunucu_UTC #utc farkını hesapla
zaman_farki_milisaniye = 1000*(istenen_utc*60*60)
#utc farkı ile zaman farkını milisaniye olarak hesapla
milliseconds = milliseconds + zaman_farki_milisaniye
saat = str(milliseconds)

if(UTC < 0):
    message = (saat+" UTC"+str(UTC))
elif(UTC >= 0):
    message = (saat+" UTC+"+str(UTC))

conn.send(message.encode('utf8'))

print("Cevap gönderildi..\n")  
conn.close()
print("baglanti sonlandi..\n")
