# Emin Sekmenoglu - 130401091
import socket, os

test_ip = "127.0.0.1"
port = 142

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((test_ip, port))

mesaj = "Test"
sock.send(mesaj.encode())
data = sock.recv(1024)
sock.send('True'.encode())
data = sock.recv(1024)
cevap = data.decode()
sock.close()

dizi = str(cevap).split(",")
utc = dizi[1]
dizi = dizi[0].split(" ")
zaman = dizi[1]
dizi = dizi[0].split("-")
tarih = str(dizi[2]) + '/' + str(dizi[1]) + '/' + str(dizi[0])
print("UTC = ", utc, "Saat = ", zaman, "Tarih = ", tarih)
calistir = 'sudo date -s ' + '"' + str(tarih) + ' ' + str(zaman) + '"'
os.system(calistir)