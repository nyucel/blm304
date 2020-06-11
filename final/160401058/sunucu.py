import socket
from time import time, gmtime
import sys

ip = str(socket.gethostbyname(socket.gethostname()))
address = (ip, 142)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

TIMEZONE = "UTC+0"

tsc = int(TIMEZONE[3:])*60*60*1000
def time_ms(): return int(round(time()*1000))+tsc


print('Server baslatildi: IP: %s Port: %s' % address)


sock.bind(address)
sock.listen(1)

while True:
    con, clientad = sock.accept()

    print("Baglanti:", clientad)
    data = con.recv(1024).decode()

    if data == "0":
        a = time_ms()
        d = str(a)+"/"+TIMEZONE
        con.send(d.encode())
        s = gmtime(int(a)/1000)
        
    else:
        break
    con.close()

sock.close()
