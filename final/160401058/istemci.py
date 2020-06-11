import sys
import socket
import time
import subprocess
import shlex
from _datetime import datetime
from timeit import default_timer as timer


ip = str(input("IP adresi girin: "))
server = (ip, 142)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((ip, 142))


sock.send("0".encode())
bas = timer()
data = sock.recv(1024).decode()
son = timer()
gecikme = (son-bas)*1000
timems, TIMEZONE = data.split("/")
timems = int(timems)+gecikme
zaman = time.gmtime(int(timems)/1000)
date = (zaman.tm_year, zaman.tm_mon, zaman.tm_mday, zaman.tm_hour,
        zaman.tm_min, zaman.tm_sec, int(timems % 1000))
print("Saat ayarlaniyor: ", datetime(
    *date).isoformat(), " Timezone: ", TIMEZONE)

tarih_saat = datetime(*date).isoformat()
subprocess.call(shlex.split("timedatectl set-ntp false"))
subprocess.call(shlex.split("sudo date -s '%s'" % tarih_saat))
subprocess.call(shlex.split("sudo hwclock -w"))
print("Sistem saati ayarlandi")


sock.close()
