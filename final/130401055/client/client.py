# Nurşah Koç 130401055
import socket
import os
import sys
import time


TCP_IP = sys.argv[1]
# TCP_IP =  [buraya sunucu IP yazilarak ustteki satir yoruma donusturulebilir.]
TCP_PORT = 142
BUFFER_SIZE = 1024

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))

except socket.error:
    print("Soket hatasi.")
    sys.exit()

ilk = time.time()
veriE = s.recv(BUFFER_SIZE)
son = time.time()
gecikme = son - ilk
veri = veriE.decode()
veriD = veri.split(" ")
zaman = float(veriD[0]) + gecikme
a = "%s"
charproblem = (a, zaman)
os.system("sudo date +%s -s @%s" % charproblem)
print("time as timestamp: ", veri)

s.close()
