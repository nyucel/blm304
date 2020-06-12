# Emin Sekmenoglu - 130401091
import socket
from datetime import datetime

test_ip = "127.0.0.1"
port = 142
UTC = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((test_ip, port))
sock.listen(10)


while (True):
    baslangic = datetime.utcnow()
    konum = datetime.now()
    gecikme_baslangic = datetime.now()
    sonuc = konum - baslangic
    sonuc = str(sonuc).split(",")

    if (len(hesap) > 1):
        yeni_sonuc = str(sonuc[1]).split(":")
        yeni_sonuc = 24 - int(yeni_sonuc[0])
        UTC = 'UTC-' + str(yeni_sonuc)

    else:
        yeni_sonuc = str(sonuc).split(":")
        UTC = 'UTC+' + str(yeni_sonuc[0])[2:]

    gonder = str(konum) + ',' + str(UTC)
    data, adr = sock.accept()

    cihaz_ip= adr[0]
    cihaz_port= adr[1]

    while (True):
        mesaj = data.recv(1024).decode()
        data.send(gonder.encode())
        yeni_mesaj = data.recv(1024).decode()
        gecikme_baslangic_son = datetime.now()
        hesaplama = (gecikme_baslangic_son - gecikme_baslangic) / 2

        mesaj = str(gecikme_baslangic_son + gecikme_baslangic) + ',' + str(UTC)
        data.send(mesaj.encode())
    data.close()