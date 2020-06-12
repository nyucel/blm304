import socket
import datetime
import os
import sys

serverIP = str(input("Sunucu adresi giriniz:"))
port = 142

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_connection = (serverIP, port) 
s.connect(server_connection)

server_time = s.recv(1024).decode()
server_timezone = s.recv(1024).decode()
time = datetime.datetime.fromtimestamp(int(server_time)/1000)
print("Yeni İstemci Zamanı: ", datetime.datetime.fromtimestamp(int(server_time)/1000).strftime('%Y-%m-%d %H:%M:%S:%f')[:-4], "İstemci Zaman Dilimi:", server_timezone)
cmd = "sudo timedatectl set-time '%s'"%time
os.system(cmd)
print("Saat değiştirildi.")
