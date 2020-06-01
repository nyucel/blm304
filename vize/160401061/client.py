import socket
import os
import sys

port = int(input("Port giriniz: "))
host = input("IP giriniz: (127.0.0.1)")
s = socket.socket()
s.connect((host, port))
kmt = s.recv(1024)
kmt = kmt.decode("utf-8")

while True:
    kmt = ("Komut Girin(GET/PUT):")
    cclient = kmt.encode("utf-8")

    try:
        s.sendto(cclient,(host, port))
    except ConnectionResetError:
        print("HATA.")
        sys.exit()
    yc = kmt.split()
    if yc[0] == "get":
        try:
            cdata, caddr = s.recvfrom(51200)
        except ConnectionResetError:
            print("HATA.")
            sys.exit()
    elif yc[0] == "put":
        try:
            cdata, caddr = s.recvfrom(4096)
        except ConnectionResetError:
            print("HATA.")
            sys.exit()
    elif yc[0] == "ls":
        try:
            cdata, caddr = s.recvfrom(51200)
        except ConnectionResetError:
            print("HATA.")
            sys.exit()
print("Program sonlanıyor.")
quit()
