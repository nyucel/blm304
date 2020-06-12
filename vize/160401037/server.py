#Kadir ÇOLAK 160401037


from socket import *
import sys
import os
import struct

sock = socket(AF_INET, SOCK_DGRAM)

print('ip :', end =" ")
server_ip = input()
server_address = (server_ip, 42)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)
while True:
    data, address = sock.recvfrom(4096)
    if data.decode() == "list":
        filelist = ""
        files = os.listdir("./files")
        for file in files:
            filelist += "- " + file + "\n"
        sent = sock.sendto(filelist.encode(), address)
    elif data.decode().startswith("get") == True:
        sp = data.decode().split(":")
        if os.path.exists("files/" + sp[1]) == False:
            sent = sock.sendto("err:notfound".encode(), address)
            continue
        f = open("files/" + sp[1],"rb")
        data = f.read(1024)
        while (data):
            if(sock.sendto(data, address)):
                data = f.read(1024)
        sock.sendto("--ENDFILE--".encode(), address)
        f.close()
    elif data.decode().startswith("put") == True:
        sp = data.decode().split(":")
        sent = sock.sendto("continue".encode(), address)
        data, address = sock.recvfrom(1024)
        f = open('files/'+sp[1],'wb')
        data,addr = sock.recvfrom(1024)
        try:
            while(data):
                if data.find("--ENDFILE--".encode()) == -1:
                    f.write(data)
                else:
                    f.write(data[:data.find("--ENDFILE--".encode())])
                    f.close()
                    sock.settimeout(999999)
                    break
                sock.settimeout(2)
                data,addr = sock.recvfrom(1024)
        except timeout:
            sock.settimeout(999999)
            f.close()
            if data.find("--ENDFILE--".encode()) == -1:
                print("Transfer Error!")
        continue
