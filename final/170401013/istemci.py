#--Bircan ARSLAN 170401013

import socket, datetime, os, sys
from datetime import datetime

hedefIP =str(input("Bağlanmak istediğiniz sunucun IP adresini giriniz:"))
port = 142
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server = hedefIP, port
    conn.connect(server)
except socket.gaierror:
    print("Hata! Lütfen bağlanmak istediğiniz sunucun IP adresini kontrol edip tekrar deneyiniz.")
    sys.exit()

sunucudate = conn.recv(1024).decode()
sunucuutc = conn.recv(1024).decode()
zaman = datetime.fromtimestamp(int(sunucudate)/1000)

print("İstemci Yeni Tarih ve Saati: ", datetime.fromtimestamp(int(sunucudate)/1000).strftime('%Y-%m-%d %H:%M:%S'), "İstemcinin Bulunduğu Zaman Dilimi:", sunucuutc)
cmd = "sudo timedatectl set-time '%s'"%zaman
os.system(cmd)

print("Saat değiştirme başarılı!")

