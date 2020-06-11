import sys
import socket
import time
from _datetime import datetime
from timeit import default_timer as timer

def linuxsetdate(date):
    import subprocess
    import shlex

    dates=datetime(*date).isoformat()

    subprocess.call(shlex.split("timedatectl set-ntp false"))
    subprocess.call(shlex.split("sudo date -s '%s'" % dates))
    subprocess.call(shlex.split("sudo hwclock -w"))
    return

port=142
buff=1024

while True:
    ip=str(input("IP adresi girin: "))
    server=(ip,port)
    if ip=="e":
        sys.exit()
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        sock.connect(server)
    except:
        print("Sunucu bulunamadi.\nTekrar deneyin. (Cikis icin 'e')")
    else:
        break

sock.send("0".encode())
bas=timer()
data=sock.recv(buff).decode()
son=timer()
gecikme=(son-bas)*1000
timems,TIMEZONE=data.split("/")
timems=int(timems)+gecikme
s=time.gmtime(int(timems)/1000)
date=(s.tm_year,s.tm_mon,s.tm_mday,s.tm_hour,s.tm_min,s.tm_sec,int(timems%1000))
print("Sistem saati ayarlaniyor: ",datetime(*date).isoformat()," Timezone: ",TIMEZONE)   
if sys.platform == 'linux2' or sys.platform == 'linux': 
    try:
        linuxsetdate(date)
    except:
        print("Sistem saati ayarlanamadi")
    else:
        print("Sistem saati ayarlandi")
sock.close()