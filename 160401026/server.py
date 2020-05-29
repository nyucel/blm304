#160401026 -- Kerim ULUSOY

import socket
import os

soket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print('ip giriniz:', end =" ")
sunucu_ip = input()
sunucu_address = (sunucu_ip, 42)
print('starting up on %s port %s' % sunucu_address)
soket.bind(sunucu_address)
while True:
    data, address = soket.recvfrom(4096)
    if data.decode() == "list":
        dosya_listesi = ""
        dosyalar = os.listdir("./dosyalar")
        for file in dosyalar:
            dosya_listesi += "- " + file + "\n"
        sent = soket.sendto(dosya_listesi.encode(), address)
    elif data.decode().startswith("get") == True:
        sp = data.decode().split(":")
        if os.path.exists("dosyalar/" + sp[1]) == False:
            sent = soket.sendto("err:notfound".encode(), address)
            continue
        f = open("dosyalar/" + sp[1],"rb")
        data = f.read(1024)
        while (data):
            if(soket.sendto(data, address)):
                data = f.read(1024)
        soket.sendto("--ENDFILE--".encode(), address)
        f.close()
    elif data.decode().startswith("put") == True:
        sp = data.decode().split(":")
        sent = soket.sendto("continue".encode(), address)
        data, address = soket.recvfrom(1024)
        f = open('dosyalar/'+sp[1],'wb')
        data,addr = soket.recvfrom(1024)
        try:
            while(data):
                if data.find("--ENDFILE--".encode()) == -1:
                    f.write(data)
                else:
                    f.write(data[:data.find("--ENDFILE--".encode())])
                    f.close()
                    soket.settimeout(999999)
                    break
                soket.settimeout(2)
                data,addr = soket.recvfrom(1024)
        except socket.timeout:
            soket.settimeout(999999)
            f.close()
            if data.find("--ENDFILE--".encode()) == -1:
                print("Transfer Error!")
        continue
