#Batuhan METİN - 160401075

import socket
import time
import os
import sys


"""Server IP'si"""
host = "192.168.1.39"
port = 42
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Socket baslatildi.")
    s.setblocking(0)
    s.settimeout(60)
except socket.error:
    print("hata")
    sys.exit()


while True:
    command = input("Bir komut girin: \n1. get [DosyaAdi]\n2. put [DosyaAdi]\n3. list\n4. exit\n ")

    CommClient = command.encode('utf-8')
    try:
        s.sendto(CommClient, (host, port))
    except ConnectionResetError:
        print("Port numarası eslesmedi")
        sys.exit()

    Client1 = command.split()

    if Client1[0] == "get":
        print("kontrol ediliyor.")
        try:
            ClientData, clientAddr = s.recvfrom(51200)
        except ConnectionResetError:
            print(
                "Port numarası eslesmedi")
            sys.exit()
        except:
            print("zaman asimi hatasi")
            sys.exit()
        text = ClientData.decode('utf8')
        print(text)


        try:
            ClientData2, clientAddr2 = s.recvfrom(51200)
        except ConnectionResetError:
            print("Port numarası eslesmedi.")
            sys.exit()
        except:
            print("zaman asimi hatasi.")
            sys.exit()

        text2 = ClientData2.decode('utf8')
        print(text2)

        if len(text2) < 30:
            if Client1[0] == "get":
                BigC = open(Client1[1], "wb")
                d = 0
                try:
                    CountC, countaddress = s.recvfrom(4096)
                except ConnectionResetError:
                    print("Port numarası eslesmedi.")
                    sys.exit()
                except:
                    print("zaman asimi hatasi.")
                    sys.exit()

                tillC = CountC.decode('utf8')
                tillCC = int(tillC)
                print("Paketler alinmaya basliyor")

                while tillCC != 0:
                    ClientBData, clientbAddr = s.recvfrom(4096)
                    dataS = BigC.write(ClientBData)
                    d += 1
                    print("paket numarası:" + str(d))
                    tillCC = tillCC - 1

                BigC.close()


    elif Client1[0] == "put":
        print("kontrol ediliyor.")
        try:
            ClientData, clientAddr = s.recvfrom(51200)
        except ConnectionResetError:
            print(
                "Port numarası eslesmedi.")
            sys.exit()
        except:
            print("Paketler alinmaya basliyor")
            sys.exit()

        text = ClientData.decode('utf8')
        print(text)
        print("Gonderim baslıyor.")

        if text == "okay":
            if os.path.isfile(Client1[1]):

                c = 0
                size = os.stat(Client1[1])
                sizeS = size.st_size
                print("byte: " + str(sizeS))
                Num = int(sizeS / 4096)
                Num = Num + 1
                print("Paket numarasi: " + str(Num))
                till = str(Num)
                tillC = till.encode('utf8')
                s.sendto(tillC, clientAddr)
                tillIC = int(Num)
                GetRun = open(Client1[1], "rb")

                while tillIC != 0:


                    Run = GetRun.read(4096)
                    s.sendto(Run, clientAddr)
                    c += 1
                    tillIC -= 1
                    print("paket numarası:" + str(c))
                    print("Veri gönderiliyor:")

                GetRun.close()

            else:
                print("Dosya bulunamadi")
        else:
            print("gecersiz")

    elif Client1[0] == "list":
        print("kontrol ediliyor.")
        try:
            ClientData, clientAddr = s.recvfrom(51200)
        except ConnectionResetError:
            print(
                "Port numarası eslesmedi.")
            sys.exit()
        except:
            print("zaman asimi hatasi.")
            sys.exit()

        text = ClientData.decode('utf8')
        print(text)

        if text == "okay":
            ClientDataL, clientAddrL = s.recvfrom(4096)
            text2 = ClientDataL.decode('utf8')
            print(text2)
        else:
            print("Hata")

    elif Client1[0] == "exit":
        print("cikildi")
    else:
        try:
            ClientData, clientAddr = s.recvfrom(51200)
        except ConnectionResetError:
            print(
                "Port numarası eslesmedi.")
            sys.exit()
        except:
            print("zaman asimi hatasi.")
            sys.exit()
        text = ClientData.decode('utf8')
        print(text)

quit()
