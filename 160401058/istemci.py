import socket
import os
import sys
PORT=int(input("Port giriniz "))
HOST = input("IP giriniz: (127.0.0.1)")

s = socket.socket()
s.connect((HOST, PORT))

cur_dir = s.recv(1024)
cur_dir = cur_dir.decode("utf-8")
while True:
    print("\nKOMUTLAR:\nls=listele\nput:sunucuya dosya yükle\nget:sunucudan dosya çek\n")
    cmd = input(str("ftp@ ") + str(cur_dir) + " > ")
    s.send(str.encode(cmd))
    s_cmd = cmd.split(" ")
    cm = s_cmd[0]

    try:
        fname = s_cmd[1]
    except:
        fname = ""

    if cm == "ls":
        size = s.recv(2)
        
        print("Dosya sayısı", size.decode("utf-8"))
        i=0
        for i in range(int(size)):
            
            data = s.recv(1024)
            s.send(str.encode("ok"))
            if not data:
                break
            data = data.decode("utf-8")
            print(data)

    if cm == "get":
        if fname == ".":
            s.send(str.encode("$all_$"))
            n = s.recv(10)
            ssize = s.recv(20)
            s.send(str.encode("ok"))
            for i in range(int(ssize)):
                fff_name = s.recv(100)
                fff_name = fff_name.decode("utf-8")
                s.send(str.encode("ok"))
                with open('serverden_gelen_'+fff_name, 'wb') as f:
                    data = s.recv(1024)
                    while True:
                        f.write(data)
                        s.send(str.encode("ok"))
                        data = s.recv(1024)
                        if data.decode("utf-8") == "$end$":
                            print(data.decode("utf-8"))
                            break
        else:
            s.send(str.encode("$one_$"))
            n = s.recv(10)
            should_try = s.recv(20)
            if should_try.decode("utf-8") == "$present$":
                s.send(str.encode("ok"))
                with open('yeni_'+fname, 'wb') as f:
                    data = s.recv(1024)
                    while True:
                        f.write(data)
                        s.send(str.encode("ok"))
                        data = s.recv(1024)
                        if data.decode("utf-8") == "$end$":
                            print(data.decode("utf-8"))
                            break
            else:
                print(should_try.decode("utf-8"))

    if cm == "put":
        if fname == ".":
            s.send(str.encode("$all$"))
            n = s.recv(10)
            path = os.getcwd()
            all_files = [f for f in os.listdir(path)
                         if os.path.isfile(os.path.join(path, f))]

            ssize = len(all_files)
            s.send(str.encode(str(ssize)))
            n = s.recv(10)
            for a_file in all_files:
                s.send(str.encode(str(a_file)))
                n = s.recv(10)
                with open(str(a_file), "rb") as f:
                    l = f.read(1024)
                    while (l):
                        s.send(l)
                        n = s.recv(10)
                        print('Sent ', repr(n))
                        l = f.read(1024)
                    s.send(str.encode("$end$"))
        else:
            if fname == "":
                print("Dosya ismi gir")
            else:
                s.send(str.encode("$one$"))
                cur_path = os.getcwd()
                if os.path.exists(fname):
                    with open(fname, "rb") as f:
                        l = f.read(1024)
                        while (l):
                            s.send(l)
                            n = s.recv(10)
                            print('Sent ', repr(n))
                            l = f.read(1024)
                        s.send(str.encode("$end$"))
                else:
                    print("Böyle bir dosya yok", fname)

   
