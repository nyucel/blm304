import socket
from time import time,gmtime
import sys

ip=str(socket.gethostbyname(socket.gethostname()))
port=142
address=(ip,port)
buff=1024
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

TIMEZONE="UTC+0" #Zaman dilimini yalnızca UTC olarak alıyor
if TIMEZONE[:3]!="UTC" or (TIMEZONE[3]!="-" and TIMEZONE[3]!="+"):
    print("TIMEZONE degiskeni yanlis formatta")
    sys.exit()

tsc=int(TIMEZONE[3:])*60*60*1000
time_ms=lambda:int(round(time()*1000))+tsc

print('Server baslatildi: IP: %s Port: %s' %address)


sock.bind(address)
sock.listen(1)

while True:
    print("Baglanti bekleniyor...")
    con,clientad=sock.accept()
    
    print("Baglanti:",clientad)
    data = con.recv(buff).decode()
        
    if data=="0":
        a=time_ms()
        d=str(a)+"/"+TIMEZONE
        con.send(d.encode())
        s=gmtime(int(a)/1000)
        print(s.tm_mday,"/",s.tm_mon,"/",s.tm_year," ",s.tm_hour,":",s.tm_min,":",s.tm_sec,":",int(a%1000)," gonderildi")
    else:
        break
    con.close()

sock.close()