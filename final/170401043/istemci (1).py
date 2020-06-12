import socket
import datetime
import os

host=input("Sunucu Ip giriniz: ")
port=142

#Merve Öztürk 170401043

sock=socket.socket()

try:
    sock.connect((host, port))

    cevap=sock.recv(1024).decode()
    zaman = cevap.split(" ")
    saat=float(zaman[0])
    tarih=datetime.datetime.fromtimestamp(saat)
    print("zaman: ",tarih," ",saat)
    sock.close()
except socket.error as mesaj:
    print("bir hata oluştu \nMesaj: ", mesaj)


islem = 'sudo date --set='
islem = islem+zaman[0]
os.system(islem)