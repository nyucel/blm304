#-----------İSTEMCİ---------------------
#160401024 Adem Çelik
import socket
import os
import datetime

host =input("Sunucu IP'si 127.0.0.1\nIp giriniz : ")
port = 142

s = socket.socket()

try:
    # Bağlantıyı yap
    s.connect((host, port))

    # serverden yanıtı al
    yanit = s.recv(1024).decode()
    zaman = yanit.split(" ")
    saat = float(zaman[0])
    bugun = datetime.datetime.fromtimestamp(saat)
    print(bugun,"  ",zaman[1])

    # bağlantıyı kapat
    s.close()
except socket.error as msg:
    print("[Server aktif değil.] Mesaj:", msg)

komut='sudo date --set='
komut = komut + zaman[0]
os.system(komut)