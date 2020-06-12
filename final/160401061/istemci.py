import socket
import os

IP = input("IP adresi girin:")
PORT = 142
print("IP = ",IP)
print("PORT = ",PORT)

try:
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print("Sunucu ile bağlanılıyor.")
    s.connect((IP, PORT))
except socket.error:
    print("Hata!",socket.error)
    s.close()

veri = s.recv(1024)
s.send('True'.encode())
veri = s.recv(1024)
mesaj = veri.decode()
print("Gelen Mesaj:",mesaj)
s.close()

z = str(mesaj).split(",")
UTC = z[1]
z = z[0].split(" ")
zaman = z[1]
z = z[0].split("-")
date = str(z[2])+'/'+str(z[1])+'/'+str(z[0])
print("UTC = ",UTC)
print("Saat = ",zaman)
print("Tarih = ",tarih)
komut = 'sudo date -s '+'"'+str(tarih)+' '+str(zaman)+'"'
print('Komut: ',komut)
os.system(komut)
print("Saat Değiştirildi.")
