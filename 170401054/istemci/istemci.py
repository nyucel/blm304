import socket
import time
import subprocess
import shlex
import pickle
import datetime
from datetime import datetime

host = "127.0.0.1"
port = 142


baslangic=datetime.now() #Gecikmeyi hesaplamak için başlangıç saati
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host,port))


zaman,address=client.recvfrom(1024)
zaman=pickle.loads(zaman)
zaman=zaman[0]
bitis=datetime.now() #Gecikmeyi hesaplamak için bitiş saati
sonzaman=bitis.microsecond - baslangic.microsecond


#Linux'da zamanı değiştirme
zamanekleme = datetime(zaman.year,zaman.month,zaman.day,zaman.hour,zaman.minute,zaman.second,zaman.microsecond+sonzaman).isoformat()
subprocess.call(shlex.split("timedatectl set-ntp false"))
subprocess.call(shlex.split("sudo date -s '%s'" % zamanekleme))
subprocess.call(shlex.split("sudo hwclock -w"))

