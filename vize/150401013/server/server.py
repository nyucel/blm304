#!/usr/bin/env python3

#Fahrettin Orkun İncili - 150401013
import socket,os

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 42        # Port to listen on (non-privileged ports are > 1023)

current_dir=os.getcwd()
print(current_dir)
server_files=os.chdir(current_dir+"/files")
current_dir=os.getcwd()

file_names=os.listdir(current_dir)
def intersperse(list, ch):
    """İndirilebilecek dosyaların arasına istenilen karakteri koyan fonksiyon"""
    result = [ch] * (len(list) * 2 - 1)
    result[0::2] = list
    return result
"""Dosya isimlerinin arasına '-' olacak."""
file_names=intersperse(file_names,"-")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(addr," bağlandı...")

        while True:
            data = conn.recv(1024)
            choice=data.decode('utf-8')
            if not choice:
                break
            if choice=="l":

                for i in file_names:
                    conn.sendall(str.encode(i))

            elif choice=="deneme.txt":
                file=open("deneme.txt","r")
                file=file.read()
                conn.sendall(str.encode(file))
            else:
                file=open("put.txt","w")
                file=file.write(choice)



