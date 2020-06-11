# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 15:05:29 2020

@author: Baran Akçakaya-170401010
"""
import socket
import os

TCP_IP = "192.168.1.35"
TCP_PORT = 142
MESSAGE = "Hello, SERVER!"
print("IP = ",TCP_IP)
print("PORT = ",TCP_PORT)

try:
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print("Sunucu ile bağlanılıyor.")
    sock.connect((TCP_IP,TCP_PORT))
except socket.error:
    print("Hata!",socket.error)
    sock.close()
    
sock.send(MESSAGE.encode())
data = sock.recv(1024)
sock.send('True'.encode())
data = sock.recv(1024)
mesaj = data.decode()
print("Gelen Mesaj:",mesaj)
sock.close()

temp = str(mesaj).split(",")
utc = temp[1]
temp = temp[0].split(" ")
time = temp[1]
temp = temp[0].split("-")
date = str(temp[2])+'/'+str(temp[1])+'/'+str(temp[0])
print("UTC = ",utc)
print("Saat = ",time)
print("Tarih = ",date)
print("Saat ayarlanıyor...")
komut = 'sudo date -s '+'"'+str(date)+' '+str(time)+'"'
print('Komut: ',komut)
os.system(komut)
print("Saat Değiştirildi.")
