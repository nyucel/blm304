import socket
from time import *
from timeit import default_timer as timer
import sys
import subprocess
import shlex
from _datetime import datetime
IP = str(input("Lutfen sunucu IP adresini giriniz: "))   
msgFromClient       = "Saat"
bytesToSend         = str.encode(msgFromClient)
serverAddressPort   = (IP, 142) 
bufferSize          = 1024
i=0
TCPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
while True:
    print("Sunucu ile bağlantı sağlanılması bekleniyor.")
    try:
        TCPClientSocket.connect(serverAddressPort)
        print("Sunucu ile bağlantı sağlandı")
        break
    except:
        if i==5:
            print("Sunucu ile bağlantı sağlanamadı client kapatılıyor.")
            sleep(2)
            sys.close()
    i+=1
TCPClientSocket.sendall(bytesToSend)
start=timer()
ServerMesaji = TCPClientSocket.recv(bufferSize).decode().split(" ")
stop=timer()
gecikme=stop-start
sa=int(ServerMesaji[0])
UTC=ServerMesaji[1]
print("Server saati: ",sa," ms"," UTC",UTC)
yil=gmtime(sa/1000).tm_year
ay=gmtime(sa/1000).tm_mon
gun=gmtime(sa/1000).tm_mday
st=gmtime(sa/1000).tm_hour + int(UTC)
dakika=gmtime(sa/1000).tm_min
saniye=gmtime(sa/1000).tm_sec
milisaniye=sa%1000+gecikme
tarih=(int(yil),int(ay),int(gun),int(st),int(dakika),int(saniye),int(milisaniye))
tarih1=datetime(*tarih).isoformat()
subprocess.call(shlex.split("timedatectl set-ntp false"))
subprocess.call(shlex.split("sudo date -s '%s'" % tarih1))
subprocess.call(shlex.split("sudo hwclock -w"))