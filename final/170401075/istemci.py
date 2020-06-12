from socket import*
import sys
import os
import time
import datetime

def zamanDilimi():
    dt = str(datetime.datetime.now().astimezone().timetz())
    iutc = dt.strip()[15:18]
    if(iutc[1] == "0"):
        iutc = int(iutc[0] + iutc[2])
    else:
        iutc = int(iutc[0] + iutc[1] + iutc[2])
    return iutc

if(len(sys.argv) == 2):
	s = socket(AF_INET, SOCK_STREAM)
	host = sys.argv[1]
	port = 142
	buf = 1024
	s.connect((host, port))
	t1 = time.time()
	zaman = s.recv(buf)
	t2 = time.time()
	gecikme = t2 - t1
	zaman = zaman.decode()
	zaman, UTC = zaman.split(" ")
	print("Gelen msn: ", zaman)
	print("UTC ", UTC)
	print("Gecikme: ", gecikme)
	zaman = int(zaman)
	UTC = int(UTC)
	zaman = zaman - zamanDilimi() * 60 * 60 * 1000 + gecikme + UTC * 60 * 60 * 1000
	komut1 = "timedatectl set-ntp false"
	komut2 = "sudo date -s@" + str(int(zaman / 1000))
	os.system(komut1)
	os.system(komut2)
	s.close()
else:
	print("istemci.py ip_adresi seklinde calistiriniz.")
