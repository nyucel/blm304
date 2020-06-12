import socket
from datetime import datetime
from time import sleep
import socket
from datetime import timedelta
import sys
#MELİSA BAYRAMLI 140401052

host=str(socket.gethostbyname(socket.gethostname()))
port=142
BUFFERSIZE=1024
finish=datetime.now().hour
start=datetime.utcnow().hour
UTC=finish-start



try:
    tcp_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcp_socket.bind((host,port))
    print("{} nolu porta baglandi. ".format(port))
    tcp_socket.listen(5)
    print("DİNLENİYOR....")

except :
    print("BAGLANAMADİ....")
    sys.exit()




while True:

    conn,address=tcp_socket.accept()
    print("Baglandi..")
    print("Zaman dilimini değiştirmek için 2 YE basin.")
    print("Var olan zamandilimi {}  ".format(UTC))

    if input() == "2":
            UTC = input("Yeni zaman dilimini girin :")
            UTC = float(UTC) / 100
            print("Yeni UTC+{}".format(UTC))

    delay=datetime.utcnow().timestamp()
    conn.send(str(delay).encode())
    delay = datetime.utcnow().timestamp() - float(conn.recv(BUFFERSIZE))

    date = (datetime.utcnow().timestamp() + delay + 0.0002) * 1000
    date += (UTC / 1) * 3600000 + (UTC % 1) * 60000

    conn.send(str(date).encode())
    sleep(0.0002)
    conn.send(str(UTC).encode())

