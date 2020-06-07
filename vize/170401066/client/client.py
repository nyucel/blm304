'''
Atakan Ayaşlı 170401066
'''
import socket
import time
import os
import sys
port=42

def ipkontrol():
    if len(sys.argv) != 2:
        print(
            "Lütfen ip ile beraber giriniz( Örnek= client.py 127.0.0.1 )")
        sys.exit()
ipkontrol()
try:
    socket.gethostbyname(sys.argv[1])
except socket.error:
    print("Host adresi yanlış.")
    sys.exit()
host = sys.argv[1]
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setblocking(0)
    s.settimeout(15)
except socket.error:
    print("Socket yaratılamadı.")
    sys.exit()

while True:
    command = input(
        "Komut giriniz: \n1. LİSTE \n2. PUT dosya_adı\n3. GET dosya_adı\n4. exit\n ")

    CommClient = command.encode('utf-8')
    try:
        s.sendto(CommClient, (host, port))
    except ConnectionResetError:
        print(
            "Porn numaraları uyuşmuyor")
        sys.exit()
    CL = command.split()

    if CL[0] == "GET":
        try:
            ClientData, clientAddr = s.recvfrom(51200)
        except ConnectionResetError:
            print(
                "Port numaraları uyuşmuyor.")
            sys.exit()
        except:
            print("Bilinmeyen hata")
            sys.exit()
        text = ClientData.decode('utf8')
        print(text)
        try:
            ClientData2, clientAddr2 = s.recvfrom(51200)
        except ConnectionResetError:
            print(
                "Port numaraları uyuşmuyor.")
            sys.exit()
        except:
            print("bilinmeyen hata")
            sys.exit()

        text2 = ClientData2.decode('utf8')
        print(text2)

        if len(text2) < 30:
            if CL[0] == "GET":
                BigC = open("Alınan-" + CL[1], "wb")
                d = 0
                try:

                    CountC, countaddress = s.recvfrom(4096)
                except ConnectionResetError:
                    print(
                        "Port numaraları uyuşmuyor.")
                    sys.exit()
                except:
                    print("bilinmeyen hata")
                    sys.exit()

                tillC = CountC.decode('utf8')
                tillCC = int(tillC)
                print("Dosya var ise paketler alınmaya başlıcak.")

                while tillCC != 0:
                    ClientBData, clientbAddr = s.recvfrom(4096)
                    dataS = BigC.write(ClientBData)
                    d += 1
                    print("Paket numarası:" + str(d))
                    tillCC = tillCC - 1

                BigC.close()
    elif CL[0] == "PUT":

        try:
            ClientData, clientAddr = s.recvfrom(4096)
        except ConnectionResetError:
            print(
                "Port numaraları uyuşmuyor.")
            sys.exit()
        except:
            print("Bilinmeyen Hata")
            sys.exit()

        text = ClientData.decode('utf8')
        print(text)
        print("Gönderim başlıyor.")

        if text == "PUT komutu kabul edildi ":
            if os.path.isfile(CL[1]):
                c = 0
                size = os.stat(CL[1])
                sizeS = size.st_size
                print("Dosay boyutu: " + str(sizeS))
                Num = int(sizeS / 4096)
                Num = Num + 1
                print("Gönderilicek paket sayısı " + str(Num))
                till = str(Num)
                tillC = till.encode('utf8')
                s.sendto(tillC, clientAddr)
                tillIC = int(Num)
                GetRun = open(CL[1], "rb")

                while tillIC != 0:
                    Run = GetRun.read(4096)
                    s.sendto(Run, clientAddr)
                    c += 1
                    tillIC -= 1
                    print("Paket:" + str(c))
                GetRun.close()
                print("Sent from Client - Put function")
            else:
                print("Dosya yok.")
        else:
            print("Kabul edilmeyen.")

    elif CL[0] == "LİSTE":

        try:
            ClientData, clientAddr = s.recvfrom(51200)
        except ConnectionResetError:
            print(
                "Port numaraları uyuşmuyor.")
            sys.exit()
        except:
            print("Bilinmeyen Hata")
            sys.exit()

        text = ClientData.decode('utf8')
        print(text)

        if text == "LİSTE komutu kabul edildi.":
            ClientDataL, clientAddrL = s.recvfrom(4096)
            text2 = ClientDataL.decode('utf8')
            print(text2)
        else:
            print("Bilinmeyen Hata.")

    elif CL[0] == "exit":
        print(
            "Çıkış yapılacak.")

    else:
        try:
            ClientData, clientAddr = s.recvfrom(51200)
        except ConnectionResetError:
            print(
                "Port numaraları uyuşmuyor.")
            sys.exit()
        except:
            print("Bilinmeyen Hata.")
            sys.exit()
        text = ClientData.decode('utf8')
        print(text)
quit()
