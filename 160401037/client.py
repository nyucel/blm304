#Kadir ÇOLAK 160401037
from socket import *
import os
import sys
import struct

sock = socket(AF_INET, SOCK_DGRAM)

print('ip :', end =" ")
server_ip = input()
server_address = (server_ip, 42)
while True:
    print('0 - disconnect')
    print('1 - list')
    print('2 - get')
    print('3 - put')
    print("request :", end =" ")
    p = input()
    if p == "1":
        sent = sock.sendto("list".encode(), server_address)
        data, server = sock.recvfrom(4096)
        print('\nfile list : \n%s' % data.decode())
    elif p == "2":
        print('filename :', end =" ")
        filename = input()
        sent = sock.sendto(("get:"+filename).encode(), server_address)
        f = open(filename,'wb')
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
    elif p == "3":
        print('filename :', end =" ")
        filename = input()
        if os.path.exists(filename) == False:
            print("Error : " + filename + " not found!")
            continue
        sent = sock.sendto(("put:"+filename).encode(), server_address)
        data,addr = sock.recvfrom(1024)
        sent = sock.sendto("continue".encode(), server_address)
        f = open(filename,"rb")
        data = f.read(1024)
        while (data):
            if(sock.sendto(data, server_address)):
                data = f.read(1024)
        sock.sendto("--ENDFILE--".encode(), server_address)
        f.close()
        continue
    elif p == "0":
        sock.close()
        break
    else:
        continue
