#Hakan Reşit YALÇIN     -   160401036

import socket
import os
import sys

PORT=int(input("PORT NUMARASINI GİRİNİZ :    "))
HOST = input("HOST GİRİNİZ :    ")

server_socketi = socket.socket()
server_socketi.connect((HOST, PORT))
cur_dir = server_socketi.recv(1024)
cur_dir = cur_dir.decode("utf-8")

while True:
    print("\n\t  - - - - KOMUTLAR - - - - \n\t ls : LISTELEME KOMUTU \n\t put [isim.uzantı] : DOSYA YÜKLEME \n\t get [isim.uzantı] : DOSYA ÇEKME \n")
    cmd = input(str("ftp@ ") + str(cur_dir) + " > ")
    server_socketi.send(str.encode(cmd))
    s_cmd = cmd.split(" ")
    cm = s_cmd[0]

    try:
        d_ismi = s_cmd[1]
    except:
        d_ismi = ""

    if cm == "ls":
        size = server_socketi.recv(2)
        
        print("Dizindeki dosya adeti :", size.decode("utf-8"))
        i=0
        for i in range(int(size)):
            
            veri = server_socketi.recv(1024)
            server_socketi.send(str.encode("ok"))
            if not veri:
                break
            veri = veri.decode("utf-8")
            print(veri)

    if cm == "get":
        if d_ismi == ".":
            server_socketi.send(str.encode("$all_$"))
            n = server_socketi.recv(10)
            ssize = server_socketi.recv(20)
            server_socketi.send(str.encode("SUCCESS"))
            for i in range(int(ssize)):
                fff_name = server_socketi.recv(100)
                fff_name = fff_name.decode("utf-8")
                server_socketi.send(str.encode("SUCCESS"))
                with open('sunucudan_gelen_'+fff_name, 'wb') as f:
                    veri = server_socketi.recv(1024)
                    while True:
                        f.write(veri)
                        server_socketi.send(str.encode("SUCCESS"))
                        veri = server_socketi.recv(1024)
                        if veri.decode("utf-8") == "SUCCESS":
                            print(veri.decode("utf-8"))
                            break
        else:
            server_socketi.send(str.encode("$one_$"))
            n = server_socketi.recv(10)
            should_try = server_socketi.recv(20)
            if should_try.decode("utf-8") == "$present$":
                server_socketi.send(str.encode("SUCCESS"))
                with open('sunucudan_gelen_'+d_ismi, 'wb') as f:
                    veri = server_socketi.recv(1024)
                    while True:
                        f.write(veri)
                        server_socketi.send(str.encode("SUCCESS"))
                        veri = server_socketi.recv(1024)
                        if veri.decode("utf-8") == "$end$":
                            print(veri.decode("utf-8"))
                            break
            else:
                print(should_try.decode("utf-8"))

    if cm == "put":
        if d_ismi == ".":
            server_socketi.send(str.encode("$all$"))
            n = server_socketi.recv(10)
            path = os.getcwd()
            dosyalar = [f for f in os.listdir(path)
                         if os.path.isfile(os.path.join(path, f))]

            ssize = len(dosyalar)
            server_socketi.send(str.encode(str(ssize)))
            n = server_socketi.recv(10)
            for a_file in dosyalar:
                server_socketi.send(str.encode(str(a_file)))
                n = server_socketi.recv(10)
                with open(str(a_file), "rb") as f:
                    l = f.read(1024)
                    while (l):
                        server_socketi.send(l)
                        n = server_socketi.recv(10)
                        print("SUCCESS", repr(n))
                        l = f.read(1024)
                    server_socketi.send(str.encode("$end$"))
                    
        else:
            if d_ismi == "":
                print("Girilen dosya ismi hatalı.Tekrar deneyiniz.")
            else:
                server_socketi.send(str.encode("$one$"))
                cur_path = os.getcwd()
                if os.path.exists(d_ismi):
                    with open(d_ismi, "rb") as f:
                        l = f.read(1024)
                        while (l):
                            server_socketi.send(l)
                            n = server_socketi.recv(10)
                            print("SUCCESS", repr(n))
                            l = f.read(1024)
                        server_socketi.send(str.encode("$end$"))
                        quit(1)
                else:
                    print(d_ismi,"DOSYASI BULUNAMADI!")
