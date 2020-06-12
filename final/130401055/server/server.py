# Nurşah Koç 130401055
import socket
import time
import sys

TCP_IP = ""
TCP_PORT = 142
BUFFER_SIZE = 1024

utc_base = "03"
utc = "03"  # buraya istenen utc degeri girilebilir.
utc_fark = (int(utc_base) - int(utc)) * 60 * 60

while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_IP, TCP_PORT))

    except socket.error:
        print("Soket hatasi.")
        sys.exit()
    s.listen(1)
    conn, istemciIP = s.accept()

    try:
        stamp = time.time()
        zaman = stamp + float(utc_fark)
        if (int(utc) >= 0):
            timeutc = str(zaman) + " UTC+" + utc
        else:
            timeutc = str(zaman) + " UTC-" + utc
        timeE = timeutc.encode()
        conn.sendall(timeE)

    except:
        print("bir hata olustu")

    conn.close()
