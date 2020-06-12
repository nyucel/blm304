#Onur Karabulut - 170401076
import socket
import sys
import time
import os
import datetime


def getUtc():
    a = datetime.datetime.now()
    b = str(a.astimezone())
    c = b[26:][:3]
    d = list(c)
    if d[0] == "+":
        if d[1] == "0":
            return int(d[2])
        else:
            return int("{0}{1}".format(d[1], d[2]))
    else:
        if d[1] == "0":
            return -int(d[2])
        else:
            return -int("{0}{1}".format(d[1], d[2]))


sct = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("Server IP Adresini Giriniz")
host = str(input("IP: "))
port = 142
buf = 1024
sct.connect((host,port))
t1 = time.time()
time_now = sct.recv(buf).decode()
print(time_now)
t2 = time.time()
tn = time_now.split(" ")
ix = ((float(tn[0])) / 1000)
iutc = (int(tn[2][3:])) - getUtc() 
time_calc2 = ix + (iutc*3600)
time_calc2 = time_calc2 + (int(t1)-int(t2))
cmd = "timedatectl set-ntp false"
cmd1 = "sudo date -s@" + str(time_calc2)
cmd2 = "sudo hwclock -w"
os.system(cmd)
os.system(cmd1)
os.system(cmd2)
sct.close()
