#Gizem Özgün 160401007

#/usr/bin/python

import os
import sys
import socket


server_ip = '127.0.0.1'

conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    command = str(input("Bir komut giriniz >>>"))
    
    conn.sendto(command.encode(), (server_ip, 42))
    

    if(command.split()[0] == 'ls'):
        data, address = conn.recvfrom(4096)
        response = data.decode('utf8')
        for file in response.split(':'):
            print(file)

    elif(command.split()[0] == 'get'):
        data, address = conn.recvfrom(8192)
        response = data.decode('utf8')
        file = open(command.split()[1], "wb")
        file.write(response)
        










