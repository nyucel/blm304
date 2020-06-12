from socket import*
import datetime
import time

def zaman():
  millis = int(round(time.time() * 1000))
  return millis

s = socket(AF_INET, SOCK_STREAM)
host = ""
port = 142
buf = 1024
UTC = 5 	# UTC degeri buradan degistirilebilir
s.bind((host, port))
s.listen(1)
while True:
	print("Baglanti bekleniyor.")
	con, addr = s.accept()
	print(str(zaman()) + " " + str(UTC) + " gonderiliyor")
	gonderilecek = str(zaman()) + " " + str(UTC)
	print(datetime.datetime.fromtimestamp(int(zaman()) / 1000.0))
	con.send(gonderilecek.encode())
s.close()
