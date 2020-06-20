#Adem YILMAZ - 160401069
import socket
import subprocess
import shlex
import pickle
from datetime import datetime
host = "127.0.0.1"
port = 142


istemciSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
istemciSoc.connect((host,port))



ilk=datetime.now()
timee,address=istemciSoc.recvfrom(1024)
timee=pickle.loads(timee)
timee=timee[0]


bitis=datetime.now()
son=bitis.microsecond - ilk.microsecond


zaman = datetime(timee.year,timee.month,timee.day,timee.hour,timee.minute,timee.second,timee.microsecond+son).isoformat()
subprocess.call(shlex.split("timedatectl set-ntp false"))
subprocess.call(shlex.split("sudo date -s '%s'" % zaman))
subprocess.call(shlex.split("sudo hwclock -w"))