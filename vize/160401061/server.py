import socket
import os
import sys

host = "127.0.0.1"
port = int(input("PORT Giriniz"))

def socket_olustur():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except:
        print("Hata")

def socket_onay():
    while True:
        c, addr = s.accept()
        print(addr[0], addr[1])

def s_list():
    msg = "komut"
    msj = msg.encode("utf-8")
    s.sendto(msj, caddr)
    print("Mesaj gönderildi.")

def s_get(g):
    msg = "komut"
    msj = msg.encode("utf-8")
    s.sendto(msj, caddr)
    print("Mesaj gönderildi.")

def s_put():
    msg = "komut"
    msj = msg.encode("utf-8")
    s.sendto(msj, caddr)
    print("Mesaj gönderildi.")

    if p[0] == "put":
        BigSAgain = open(p[1], "wb")

host = ""
port = 42

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Sunucu soketi balşatıldı")
    s.bind((host, port))
    print("Bağlantı sağlandı, istemci bekleniyor")
except socket.error:
    print("Soket oluşturulamadı")
    sys.exit()

while True:
    try:
        data, caddr = s.recvfrom(4096)
    except ConnectionResetError:
        print("HATA.")
        sys.exit()
    m = data.decode("utf8")
    p = m.split()
    if p[0] == "Get":
        print("Get")
        s_get(p[1])
    elif p[0] == "Put":
        print("Put")
        s_put()
    elif p[0] == "ls":
        print("Liste")
        s_list()
print("Program sona eriyor.")
quit()
