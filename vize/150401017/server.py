#İlyas KURT-150401017
import socket
import time
import os
import sys

def ServerList():
    
    msg = "List komutu dogru."
    msgEn = msg.encode('utf-8')
    socket.sendto(msgEn, clientAddr)

    F = os.listdir(
        path="C:/Users/İlyas KURT/Desktop/150401017")
   #serverın bulundugu dosya konumunu giriniz 

    Lists = []
    for file in F:
        Lists.append(file)
    ListsStr = str(Lists)
    ListsEn = ListsStr.encode('utf-8')
    socket.sendto(ListsEn, clientAddr)
    print("Liste server tarafindan yollaniyor.")


def ServerGet(g):
    
    msg = "Get komutu dogru."
    msgEn = msg.encode('utf-8')
    socket.sendto(msgEn, clientAddr)
 
    if os.path.isfile(g):
        msg = "Dosya mevcut indiriliyor. "
        msgEn = msg.encode('utf-8')
        socket.sendto(msgEn, clientAddr)
        print("Dosya kontrol edildi.")

        c = 0
        sizeS = os.stat(g)
        sizeSS = sizeS.st_size  # paket numarası
        print("Dosya boyutu bytes:" + str(sizeSS))
        NumS = int(sizeSS / 4096)
        NumS = NumS + 1
        tillSS = str(NumS)
        tillSSS = tillSS.encode('utf8')
        socket.sendto(tillSSS, clientAddr)

        check = int(NumS)
        GetRunS = open(g, "rb")
        while check != 0:
            RunS = GetRunS.read(4096)
            socket.sendto(RunS, clientAddr)
            c += 1
            check -= 1
            print("Packet number:" + str(c))
            print("veri yollaniyor:")
        GetRunS.close()
    

    else:
        msg = "Hata:server da bu dosya mevcut degil."
        msgEn = msg.encode('utf-8')
        socket.sendto(msgEn, clientAddr)
        print("Mesaj gönderildi.")


def ServerPut():
    
    msg = "Put komutu dogru."
    msgEn = msg.encode('utf-8')
    socket.sendto(msgEn, clientAddr)
    
    if t2[0] == "put":

        dosya = open(t2[1], "wb")
        d = 0
        print("Dosya mevcut ise islem basliyor.")
        try:
            Count, countaddress = socket.recvfrom(4096)  # paket numarası
        except ConnectionResetError:
            print("Port hatasi")
            sys.exit()
        except:
            print("Zaman asimi veya diger.")
            sys.exit()

        tillI = Count.decode('utf8')
        tillI = int(tillI)

        while tillI != 0:
            ServerData, serverAddr = socket.recvfrom(4096)
            
            dataS = dosya.write(ServerData)
            d += 1
            tillI = tillI - 1
            print("packet number:" + str(d))

        dosya.close()
        print("Yeni dosya kapandi klasoru kontrol ediniz.")


def ServerElse():
    msg = "Hata. Sormus oldugunuz: " + \
        t2[0] + " bu komutun karsiligi bulunamadi"
    msgEn = msg.encode('utf-8')
    socket.sendto(msgEn, clientAddr)
    print("Message Sent.")


    
host = "127.0.0.1"
port = 42
try:
    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Server socet olusturuldu.")
    socket.bind((host, port))
    print("Baglanti basarili Istemci bekleniyor.")
    print ("host %s: port %d  "%(host,port))

except socket.error:
    print("Socket olusturmada hata")
    sys.exit()

while True:
    try:
        data, clientAddr = socket.recvfrom(4096)
    except ConnectionResetError:
        print("Port hatasi.")
        sys.exit()
    text = data.decode('utf8')
    t2 = text.split()

    if t2[0] == "get":
        ServerGet(t2[1])
    elif t2[0] == "put":
        ServerPut()
    elif t2[0] == "list":
        ServerList()
    else:
        ServerElse()

print("Program sonlandiriliyor ")
quit()
