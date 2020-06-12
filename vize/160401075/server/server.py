#Batuhan METİN - 160401075

import socket
import os
import sys

def List1():
    msg = "okay"
    msgEn = msg.encode('utf-8')
    s.sendto(msgEn, clientAddr)

    """server.py dosyanın bulunduğu dosya uzantısı yazılacak."""
    Files = os.listdir( path="C:/Users/gurka/Desktop/batuhan/server")

    Lists = []
    for file in Files:
        Lists.append(file)
    ListsStr = str(Lists)
    ListsEn = ListsStr.encode('utf-8')
    s.sendto(ListsEn, clientAddr)


def Exit1():

    print("socket kapatıldı!")
    s.close()
    sys.exit()


def Get1(g):
    msg = "okay"
    msgEn = msg.encode('utf-8')
    s.sendto(msgEn, clientAddr)

    if os.path.isfile(g):
        msg = "okay"
        msgEn = msg.encode('utf-8')
        s.sendto(msgEn, clientAddr)

        c = 0
        sizeS = os.stat(g)
        sizeSS = sizeS.st_size
        print("bytes:" + str(sizeSS))
        NumS = int(sizeSS / 4096)
        NumS = NumS + 1
        tillSS = str(NumS)
        tillSSS = tillSS.encode('utf8')
        s.sendto(tillSSS, clientAddr)

        check = int(NumS)
        GetRunS = open(g, "rb")
        while check != 0:
            RunS = GetRunS.read(4096)
            s.sendto(RunS, clientAddr)
            c += 1
            check -= 1
            print("paket numarasi:" + str(c))
            print("Veri gonderiliyor:")
        GetRunS.close()

    else:
        msg = "bitti"
        msgEn = msg.encode('utf-8')
        s.sendto(msgEn, clientAddr)

def Put1():
    msg = "okay"
    msgEn = msg.encode('utf-8')
    s.sendto(msgEn, clientAddr)

    if t2[0] == "put":

        BigSAgain = open(t2[1], "wb")
        d = 0
        print("paket alınmaya başlanıyor.")
        try:
            Count, countaddress = s.recvfrom(4096)
        except ConnectionResetError:
            print(
                "Port numarası eslesmiyor")
            sys.exit()
        except:
            print("paket zaman asımına ugradı")
            sys.exit()

        tillI = Count.decode('utf8')
        tillI = int(tillI)


        while tillI != 0:
            ServerData, serverAddr = s.recvfrom(4096)
            dataS = BigSAgain.write(ServerData)

            d += 1
            tillI = tillI - 1
            print("Paket numarasi" + str(d))

        BigSAgain.close()


def Else1():
    msg = "Error: " + t2[0] + " sunucu tarafından anlasılamadı."
    msgEn = msg.encode('utf-8')
    s.sendto(msgEn, clientAddr)

host = ""
port = 42
try:
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    print("Server socket basladi.")
    s.bind((host, port))
    print("client bekleniyor.")

except socket.error:
    print("baglantıda hata olustu.")
    sys.exit()

while True:
    try:
        data, clientAddr = s.recvfrom(4096)
    except ConnectionResetError:
        print("port numarasi eslesmedi.")
        sys.exit()

    text = data.decode('utf8')
    t2 = text.split()
    if t2[0] == "get":
        Get1(t2[1])
    elif t2[0] == "put":
        Put1()
    elif t2[0] == "list":
        List1()
    elif t2[0] == "exit":
        Exit1()
    else:
        Else1()

quit()