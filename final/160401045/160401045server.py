#Gökçe Kuler
import socket
import time
import datetime

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('0.0.0.0', 142)
print('{} port {}'.format(*server_address))
sock.bind(server_address)
sock.listen(5)

while True:
    print('bağlantı hazır')
    connection, client_address = sock.accept()
    print('adres', client_address)
    data = connection.recv(1024)
    utcsinir=datetime.datetime.utcnow()  #genel değer
    yerelzaman=datetime.datetime.now()   #yerel değer
    utcdeger=yerelzaman-utcsinir         #arasındaki fark
    i=str(utcdeger)[0]
    j="UTC+"
    UTC=j + i #utc değerini tutan değişken
    zaman=int(round(time.time()*1000))
    connection.send(str(zaman).encode())
    connection.close()















