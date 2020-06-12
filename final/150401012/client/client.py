#Yiğit Yüre 150401012

import socket
import datetime
import sys
import subprocess
import shlex

HOST = input("ip adresini giriniz : ")
PORT = input("port numarasını giriniz : ")

def settime(timetuple):
    timestring = datetime(*timetuple).isoformat()
    subprocess.call(shlex.split("timedatectl set-ntp false"))
    subprocess.call(shlex.split("sudo date -s '%s'" % timestring))
    subprocess.call(shlex.split("sudo hwclock -w"))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

sendtime = datetime.datetime.utcnow()

while True:
    data = s.recv(1024)
    receivetime = datetime.datetime.utcnow()
    difference = receivetime - sendtime
    (diftime, micro) = difference.strftime('%Y-%m-%d %H:%M:%S.%f').split('.')
    diftime = "%s.%03d" % (diftime, int(micro) / 1000)

    servertime = data.decode().split(" ")
    date = servertime[0]
    time = severtime[1]
    utc = servertime[2]

    hour = str(int(time.split(":")[0]) + int(diftime.split(" ")[1].split(":")[0]))
    minute = str(int(time.split(":")[1]) + int(diftime.split(":")[1]))
    sec = str(int(time.split(":")[2].split(".")[0]) + int(diftime.split(":")[2].split(".")[0]))
    milsec = str(int(time.split(".")[1]) + int(diftime.split(".")[1]))
    if(int(minute) > 60):
        minute = str(int(minute) - 60)
        hour = str(int(hour) + 1)
    if(int(sec) > 60):
        sec = str(int(sec) - 60)
        minute = str(int(minute) + 1)
    if(int(milsec) > 1000000):
        milsec = str(int(milsec) - 1000000)
        sec = str(int(sec) + 1)
    if(int(minute) < 10):
        minute = "0" + minute
    if(int(sec) < 10):
        sec = "0" + sec
    realtime = date + " " + hour + ":" + minute + ":" + sec + "." + milsec + " " + utc

    timetuple = (int(realtime.split("-")[0]), int(realtime.split("-")[1]), int(realtime.split(" ")[0].split("-")[2]), int(realtime.split(" ")[1].split(":")[0]), int(realtime.split(":")[1]), int(realtime.split(":")[2].split(".")[0]), int(realtime.split(" ")[1].split(".")[1]))
    settime(timetuple)

s.close()