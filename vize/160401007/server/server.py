#Gizem Özgün 160401007

#/usr/bin/python



import os
import sys
import socket

def file_list():
    path = os.getcwd()
    files = os.listdir(path)
    fileList = str()
    for file in files:
        file += ':'
        fileList += file
    return fileList

def get(filename):
    if os.path.isfile(filename):
        file = open(filename, "wb")
    
    return file

def put(filename):
    return filename


conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
conn.bind(('127.0.0.1', 42))

while True:
    try:
        data, address = conn.recvfrom(4096)
    except:
        print("Bir hata olustu")

    data = data.decode('utf8')
    command = data.split()[0]
    print(data)
    
    if(command == 'ls'):
        conn.sendto(file_list().encode(), address)

    elif(command == 'get'):
        file = get(data.split()[1])
        conn.sendto(file.encode(), address)
        file.close()

    elif(command == 'put'):
        put(data.split()[1])
    else:
        conn.sendto("Gecerli bir komut giriniz", address)
           











    
