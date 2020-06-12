#İlyas KURT-150401017
import socket
import time
import os
import sys

host = "127.0.0.1"
port = 42
try:
    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket.setblocking(0)
    socket.settimeout(15)
except socket.error:
    print("Socket olusturmada hata")
    sys.exit()
    time.sleep(1)  


while True:
    komut = input("Komutu giriniz: \n1. get [file_name]\n2. put [file_name]\n3. list\n ")

    CommClient = komut.encode('utf-8')
    try:
        socket.sendto(CommClient, (host, port))
    except ConnectionResetError:
        print("Port hatasi")
        sys.exit()
    commlist = komut.split()
    print("Bekleniyor.")
    if commlist[0] == "get":
        
        try:
            ClientData, clientAddr = socket.recvfrom(51200)
        except ConnectionResetError:
            print("Port hatasi")
            sys.exit()
        except:
            print("Zaman asimi veya diger.")
            sys.exit()
        text = ClientData.decode('utf8')
        print(text)
        print("Istemci-Get fonksiyonundan yollaniyor.")

        try:
            ClientData2, clientAddr2 = socket.recvfrom(51200)
        except ConnectionResetError:
            print("Port hatasi")
            sys.exit()
        except:
            print("Zaman asimi veya diger.")
            sys.exit()

        text2 = ClientData2.decode('utf8')
        print(text2)

        if len(text2) < 30:
            if commlist[0] == "get":
                dosya = open("new-" + commlist[1], "wb")
                d = 0
                try:
                    CountC, countaddress = socket.recvfrom(4096)
                except ConnectionResetError:
                    print("Port hatasi")
                    sys.exit()
                except:
                    print("Zaman asimi veya diger.")
                    sys.exit()

                tillC = CountC.decode('utf8')
                tillCC = int(tillC)
                
                while tillCC != 0:
                    ClientBData, clientbAddr = socket.recvfrom(4096)
                    dataS = dosya.write(ClientBData)
                    d += 1
                    print("Alinan paket numarasi" + str(d))
                    tillCC = tillCC - 1

                dosya.close()
                print("Indirme tamamlandı klasoru kontrol ediniz.")

    elif commlist[0] == "put":
        
        try:
            ClientData, clientAddr = socket.recvfrom(4096)
        except ConnectionResetError:
            print("Port hatasi")
            sys.exit()
        except:
            print("Zaman asimi veya diger.")
            sys.exit()

        text = ClientData.decode('utf8')
        print(text)
        print("veri yollanmaya baslaniyor.")

        if text == "Put komutu dogru.":
            if os.path.isfile(commlist[1]):

                c = 0
                size = os.stat(commlist[1])
                sizeS = size.st_size  # packet numarası
                print("Dosya boyutu bytes: " + str(sizeS))
                Num = int(sizeS / 4096)
                Num = Num + 1
                print("Yollanan paket numarasi: " + str(Num))
                till = str(Num)
                tillC = till.encode('utf8')
                socket.sendto(tillC, clientAddr)
                tillIC = int(Num)
                GetRun = open(commlist[1], "rb")

                while tillIC != 0:
                    Run = GetRun.read(4096)
                    socket.sendto(Run, clientAddr)
                    c += 1
                    tillIC -= 1
                    print("Packet number:" + str(c))
                    print("........")

                GetRun.close()

                print("İstemci Put fonksiyonundan yollaniyor.")
            else:
                print("Dosya mevcut degil.")
        else:
            print("Hata.")

    elif commlist[0] == "list":

        try:
            ClientData, clientAddr = socket.recvfrom(51200)
        except ConnectionResetError:
            print("Port Hatasi.")
            sys.exit()
        except:
            print("Zaman asimi veya diger.")
            sys.exit()

        text = ClientData.decode('utf8')
        print(text)

        if text == "List komutu dogru.":
            ClientDataL, clientAddrL = socket.recvfrom(4096)
            text2 = ClientDataL.decode('utf8')
            print(text2)
        else:
            print("Hata.")

   
    else:
        try:
            ClientData, clientAddr = socket.recvfrom(51200)
        except ConnectionResetError:
            print("Port Hatasi.")
            sys.exit()
        except:
            print("Zaman asimi veya diger.")
            sys.exit()
        text = ClientData.decode('utf8')
        print(text)

print("Program sonlandiriliyor. ") 
quit()
