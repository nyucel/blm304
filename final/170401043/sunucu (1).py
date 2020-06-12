import  sys
import socket
import datetime

host = '127.0.0.1'
port = 142

#Merve Öztürk 170401043
try:
    socket = socket.socket()
    print("Soket Oluşturuldu ")

    socket.bind((host,port))
    print("{} port ile bağlantı kuruldu"),format(port)
    socket.listen(5)
except socket.error as mesaj:
    print("Hata: ", mesaj)


while True:
    istemci,addr=socket.accept()
    print("Bağlantı:",addr)
    t = datetime.datetime.now()
    zaman = datetime.datetime.timestamp(t)

    ileti=str(zaman)+" UTC+2"
    istemci.send(ileti.encode())
