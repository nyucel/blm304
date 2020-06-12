import socket
import time		#Gözde Aykent 170401063

utc=3
host="127.0.0.1"
port=142

try:
    sunucu=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sunucu.bind((host,port))
    sunucu.listen(1)
    print("sunucu açıldı")
except socket.error:
    print("hata oluştu")
while True:
    data,addr=sunucu.accept()
    zaman=time.time()*1000
    data.send(str(zaman).encode('utf-8'))
    zaman2=time.time()*1000
    data.send(str(utc).encode('utf-8'))
    print("zaman dilimi ve tarih gönderildi")
    data.send(str(zaman2-zaman).encode('utf-8'))
    data.close()